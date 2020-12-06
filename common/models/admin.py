from .base import Base, db
from common.utility import *
from common.redis.redis import Redis


class Admin(Base):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), nullable=False, comment='用户名')
    password = db.Column(db.String(32), nullable=False, comment='密码')
    encryption = db.Column(db.String(6), nullable=False, comment='密文')
    nickname = db.Column(db.String(32), comment='昵称')
    remark = db.Column(db.String(255), comment="备注")

    # 外键、关联
    image_id = db.Column(db.Integer, db.ForeignKey('upload.id'))
    image = db.relationship("Upload", foreign_keys=[image_id])

    @classmethod
    def login(cls, username, password):
        admin = cls.query.filter_by(username=username, is_delete=0).first()

        if not admin: return {"status": "failure", "msg": "用户名不存在"}
        if md5(md5(password) + admin.encryption) == admin.password: return {"status": "success", "user": admin}

        return {"status": "failure", "msg": "用户名或者密码错误"}

    def logout(self):
        redis_obj = Redis()
        redis_obj.delete('admin_token_%s' % self.id)

    @classmethod
    def add(cls, username, password, password_, image_id=None, nickname="admin", remark=None):
        if password != password_:
            return {"status": "failure", "msg": "两次密码不一致"}
        exist = Admin.query.filter_by(username=username, is_delete=0).first()
        if exist:
            return {"status": "failure", "msg": "该用户名已被注册"}

        encryption = random_str(6)
        admin = Admin(
            username=username,
            password=md5(md5(password) + encryption),
            encryption=encryption,
            nickname=nickname,
            remark=remark,
            image_id=image_id
        )
        db.session.add(admin)
        db.session.commit()

        return {"status": "success", "msg": "添加成功"}

    def update(self, password=None, password_=None, image_id=None, nickname="admin", remark=None):
        data = {"image_id": image_id, "nickname": nickname, "remark": remark}
        if password is not None:
            if password != password_:
                return {"status": "failure", "msg": "两次密码不一致"}
            data['password'] = md5(md5(password) + self.encryption)

        self.set_attrs(data)
        db.session.commit()
        return {"status": "success", "msg": "修改成功"}

    def create_token(self):
        token = encrypt({"id": self.id, "type": "admin"})
        redis_obj = Redis()
        redis_obj.write('admin_token_%s' % self.id, token, current_app.config['TOKEN_EXPIRE'])
        return token

    @classmethod
    def check_token(cls, admin_id, token):
        redis_obj = Redis()
        current_token = redis_obj.read('admin_token_%s' % admin_id)

        if not current_token:
            return {"status": "failure", "msg": "token已过期"}
        if current_token != token:
            return {"status": "failure", "msg": "您的账号已在别处登录"}

        admin = cls.query.filter_by(id=admin_id, is_delete=0).first()
        return {"status": "success", "user": admin}

    @property
    def is_super(self):
        return True
