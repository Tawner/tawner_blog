from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    create_time = db.Column(db.DateTime, nullable=False, default=db.func.now(), comment='创建时间')  # 记录的创建时间
    update_time = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now(), comment='更新时间')
    is_delete = db.Column(db.SmallInteger, default=0, comment='删除标识')

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.is_delete = 1
        db.session.commit()





