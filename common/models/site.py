from .base import Base, db
from .modules import Category


class SiteInfo(Base):
    __tablename__ = "site"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), comment="网站名")
    slogan = db.Column(db.String(255), comment="标语")
    notice = db.Column(db.String(255), comment="通知")
    case_number = db.Column(db.String(255), comment="备案号")
    domain = db.Column(db.String(255), comment="域名")
    host = db.Column(db.String(255), comment="博客地址")

    # 外键关联
    avatar_id = db.Column(db.Integer, db.ForeignKey("upload.id"), comment="头像")
    avatar = db.relationship("Upload", foreign_keys=[avatar_id])
    logo_id = db.Column(db.Integer, db.ForeignKey("upload.id"), comment="logo的id")
    logo = db.relationship("Upload", foreign_keys=[logo_id])
    background_id = db.Column(db.Integer, db.ForeignKey("upload.id"), comment="logo的id")
    background = db.relationship("Upload", foreign_keys=[background_id])


class SocialContact(Base):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), comment="标题")
    icon = db.Column(db.String(128), comment="图标class")
    color = db.Column(db.String(128), comment="图标颜色")
    url = db.Column(db.String(255), comment="链接地址")
    sort = db.Column(db.SmallInteger, comment="排序值")


class Navigation(Base):
    __tablename__ = "navigation"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), comment="导航标题")
    sort = db.Column(db.SmallInteger, comment="排序值")

    @property
    def links(self):
        link_list = []
        for url in self.urls:
            if url.is_delete == 0:
                link_list.append(url)
        return link_list


class NavigationUrl(Base):
    __tablename__ = "navigation_url"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), comment="名称")
    url = db.Column(db.String(255), comment="跳转url")
    sort = db.Column(db.SmallInteger, comment="排序值")

    # 外键关联
    navigation_id = db.Column(db.Integer, db.ForeignKey("navigation.id"), comment="导航")
    navigation = db.relationship("Navigation", foreign_keys=[navigation_id], backref="urls")


class Focusing(Base):
    __tablename__ = "focusing"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    focus_id = db.Column(db.Integer, comment="聚焦内容id")
    module = db.Column(db.String(128), comment="内容所属模块")
    sort = db.Column(db.SmallInteger, comment="排序值")

    @property
    def focus(self):
        model = Category.MODULE_TYPE[self.module]
        obj = model.query.filter(model.is_delete == 0, model.published == True, model.id == self.focus_id).first()
        return obj

    @property
    def cover(self):
        return self.focus.cover.url if self.focus else None

