from .base import Base, db
from common.utility import *
from common.redis.redis import Redis


class User(Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), comment='邮箱，登录的账号')
    password = db.Column(db.String(32), nullable=False, comment='密码')
    encryption = db.Column(db.String(6), nullable=False, comment='密文')
    nickname = db.Column(db.String(32), comment='昵称')
    description = db.Column(db.String(255), comment="简介")
    gender = db.Column(db.SmallInteger, comment="0保密，1女，2男")

    # 外键、关联
    image_id = db.Column(db.Integer, db.ForeignKey('upload.id'))
    image = db.relationship("Upload", foreign_keys=[image_id])

    @classmethod
    def register(cls, email, password, password_, code):
        redis_obj = Redis()
        email_code = redis_obj.read(email)
        exist = User.query.filter_by(email=email, is_delete=0).first()

        if not email_code or email_code != code:
            return {"status": "failure", "msg": "邮箱校验失败"}
        if exist:
            return {"status": "failure", "msg": "该邮箱已被注册"}
        if password != password_:
            return {"status": "failure", "msg": "两次密码不一致"}

        encryption = random_str(6)
        user = User(email=email, password=md5(md5(password) + encryption), encryption=encryption)
        db.session.add(user)
        db.session.commit()
        redis_obj.delete(email)  # 删除邮箱code
        return {"status": "success", "msg": "注册成功"}

    @classmethod
    def login(cls, username, password):
        user = User.query.filter_by(email=username, is_delete=0).first()

        if not user:
            return {"status": "failure", "msg": "用户名不存在"}
        if md5(md5(password) + user.encryption) == user.password:
            return {"status": "success", "user": user}

        return {"status": "failure", "msg": "用户名或者密码错误"}

    def update(self, nickname=None, description=None, gender=None, image_id=None):
        self.set_attrs({"nickname": nickname, "description": description, "gender": gender, "image_id": image_id})
        db.session.commit()
        return {"status": "success", "user": self}

    def modify_password(self, password, password_, code):
        redis_obj = Redis()
        email_code = redis_obj.read(self.email)

        if not email_code or email_code != code:
            return {"status": "failure", "msg": "邮箱校验失败"}
        if password != password_:
            return {"status": "failure", "msg": "两次密码不一致"}

        self.password = md5(md5(password) + self.encryption)
        db.session.commit()
        return {"status": "success", "msg": "修改成功"}

    def logout(self):
        redis_obj = Redis()
        redis_obj.delete('user_token_%s' % self.id)

    def create_token(self):
        token = encrypt({"id": self.id, "type": "user"})
        redis_obj = Redis()
        redis_obj.write('user_token_%s' % self.id, token, current_app.config['TOKEN_EXPIRE'])
        return token

    @classmethod
    def check_token(cls, user_id, token):
        redis_obj = Redis()
        current_token = redis_obj.read('user_token_%s' % user_id)
        if not current_token: return {"status": "failure", "msg": "token已过期"}
        if current_token != token: return {"status": "failure", "msg": "您的账号已在别处登录"}
        user = User.query.filter_by(id=user_id, is_delete=0).first()
        return {"status": "success", "user": user}

    @property
    def is_super(self):
        return False

    def delete(self):
        super().delete()
        self.logout()
