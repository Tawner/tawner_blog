from .base import Base, db
from common.utility import *
from common.redis.redis import Redis


class User(Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), nullable=False, comment='用户名')
    password = db.Column(db.String(32), nullable=False, comment='密码')
    encryption = db.Column(db.String(6), nullable=False, comment='密文')
    nickname = db.Column(db.String(32), comment='昵称')
    description = db.Column(db.String(255), comment="简介")
    gender = db.Column(db.SmallInteger, comment="0保密，1女，2男")
    email = db.Column(db.String(128), comment='邮箱')
    is_super = db.Column(db.Boolean, comment="是否为后台用户")

    # 外键、关联
    image_id = db.Column(db.Integer, db.ForeignKey('upload.id'))
    image = db.relationship("Upload", foreign_keys=[image_id])

    @classmethod
    def add(cls, username, password, nickname=None, email=None, description=None, image_id=None, gender=0, is_super=False):
        exist = User.query.filter(User.username == username).first()
        if exist: return {"status": "failure", "msg": "用户名已存在"}
        encryption = random_str(6)
        user = User(
            username=username,
            password=md5(md5(password) + encryption),
            encryption=encryption,
            nickname=nickname,
            email=email,
            gender=gender,
            description=description,
            image_id=image_id,
            is_super=is_super
        )
        db.session.add(user)
        db.session.commit()
        return {"status": "success", "user": user}

    def update(self, password=None, nickname=None, email=None, description=None, gender=None, image_id=None):
        if password: self.password = md5(md5(password) + self.encryption)
        if nickname: self.nickname = nickname
        if email: self.email = email
        if description: self.description = description
        if gender: self.gender = gender
        if image_id: self.image_id = image_id
        db.session.commit()
        return {"status": "success", "user": self}

    @staticmethod
    def check_password(username, password):
        query_args = [User.username == username, User.is_delete == 0]
        user = User.query.filter(*query_args).first()
        if not user: return {"status": "failure", "msg": "用户名不存在"}
        if md5(md5(password) + user.encryption) == user.password:
            return {"status": "success", "user": user}
        else:
            return {"status": "failure", "msg": "用户名或者密码错误"}

    @classmethod
    def check_username(cls, username):
        exist = User.query.filter(User.username == username, User.is_delete == 0).first()
        return False if exist else True

    def create_token(self):
        token = encrypt({"id": self.id})
        redis_obj = Redis()
        redis_obj.write('user_token_%s' % self.id, token, current_app.config['TOKEN_EXPIRE'])
        return token

    @classmethod
    def check_token(cls, token):
        token_data = decrypt(token)
        if not token_data: return {"status": "failure", "msg": "token有误"}
        redis_obj = Redis()
        current_token = redis_obj.read('user_token_%s' % token_data['id'])
        if not current_token: return {"status": "failure", "msg": "token已过期"}
        if current_token != token: return {"status": "failure", "msg": "您的账号已在别处登录"}
        user = User.query.filter(User.id == token_data['id'], User.is_delete == 0).first()
        return {"status": "success", "user": user}

    @property
    def avatar(self):
        return self.image.url