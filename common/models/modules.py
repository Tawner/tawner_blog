from .base import Base, db
from sqlalchemy import or_


# 文章模块
class Article(Base):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False, comment="文章标题")
    content = db.Column(db.Text, comment="文章内容")
    comment = db.Column(db.Integer, comment="评论人数", default=0)
    view = db.Column(db.Integer, comment="浏览次数", default=0)
    recom = db.Column(db.Boolean, default=0, comment="是否推荐，0否1是")
    top = db.Column(db.Boolean, default=False, comment="是否置顶")
    published = db.Column(db.Boolean, default=1, comment="是否发布0否1是")
    publish_date = db.Column(db.DateTime, nullable=False, default=db.func.now(), comment='发布时间')
    description = db.Column(db.String(255), comment="文章简要描述")

    # 外键关联
    cover_id = db.Column(db.Integer, db.ForeignKey("upload.id"), comment="封面")
    cover = db.relationship("Upload", foreign_keys=[cover_id])
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), comment="栏目")
    category = db.relationship("Category", foreign_keys=[category_id])
    tags = db.relationship("Tag", secondary="article_tag")

    @property
    def hot(self):
        return True if self.view >= 200 else False

    @classmethod
    def list(cls, page=1, rows=10, word=None, category=None, recom=False, published=None):
        query_args = [Article.is_delete == 0]

        # 条件
        if word:
            query_args.append(or_(Article.title.like('%' + word + '%'), Article.content.like('%' + word + '%')))
        if category:
            cate = Category.query.get(category)
            category_ids = [cate.id].extend([lower.id for lower in cate.sub])
            query_args.append(Article.category_id.in_(category_ids))
        if recom:
            query_args.append(Article.recom == True)
        if published is not None:
            query_args.append(Article.published == published)

        # 查询
        paginate = Article.query.filter(
            *query_args
        ).order_by(Article.top.desc(), Article.publish_date.desc()).paginate(page, rows)
        return paginate


class Tag(Base):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), comment="标签名")
    sort = db.Column(db.SmallInteger, comment="排序值")
    articles = db.relationship("Article", secondary="article_tag")


class ArticleTag(Base):
    __tablename__ = "article_tag"
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), primary_key=True, comment='文章id')
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True, comment="标签id")


# 图集模块
class PictureAlbum(Base):
    __tablename__ = "picture_album"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False, comment="图集名")
    description = db.Column(db.Text, comment="图集描述")

    # 外键关联
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), comment="栏目")
    category = db.relationship("Category", foreign_keys=[category_id])
    cover_id = db.Column(db.Integer, db.ForeignKey("upload.id"), comment="封面")
    cover = db.relationship("Upload", foreign_keys=[cover_id])


class Picture(Base):
    __tablename__ = "picture"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), comment="标题")
    description = db.Column(db.Text, comment="描述")

    # 外键关联
    image_id = db.Column(db.Integer, db.ForeignKey("upload.id"))
    image = db.relationship("Upload", foreign_keys=[image_id])
    picture_album_id = db.Column(db.Integer, db.ForeignKey("picture_album.id"))
    picture_album = db.relationship("PictureAlbum", foreign_keys=[picture_album_id], backref="picture")


# 下载模块
class Download(Base):
    __tablename__ = "download"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), comment="名称")
    description = db.Column(db.Text, comment="描述")
    version = db.Column(db.String(64), comment="版本")

    # 外键关联
    file_id = db.Column(db.Integer, db.ForeignKey("upload.id"))
    file = db.relationship("Upload", foreign_keys=[file_id])
    cover_id = db.Column(db.Integer, db.ForeignKey("upload.id"), comment="封面")
    cover = db.relationship("Upload", foreign_keys=[cover_id])


# 栏目
class Category(Base):
    MODULE_TYPE = {
        "article": Article,
        "picture": PictureAlbum,
        "download": Download
    }
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False, comment="栏目名")
    level = db.Column(db.SmallInteger, comment="栏目等级")
    sort = db.Column(db.SmallInteger, default=20, comment="排序值")
    module = db.Column(db.String(32), comment="所属模块")

    # 外键关联
    upper_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    upper = db.relationship("Category", foreign_keys=[upper_id], backref="lower")

    def empty(self):
        """是否为空栏目"""
        model = self.MODULE_TYPE[self.module]
        sub = model.query.filter(model.is_delete == 0, model.category_id == self.id).all()
        delete_tag = [lower.is_delete for lower in self.lower]
        return True if not sub and not all(delete_tag) else False

    @property
    def sub(self):
        self.lower.sort(key=lambda x: x.sort)
        lower_list = []
        for lower in self.lower:
            if lower.is_delete == 0:
                lower_list.append(lower)
        return lower_list

    @classmethod
    def add(cls, title, sort=20, module=None, upper_id=None):
        data = {"title": title, "sort": sort}
        if upper_id:
            upper = Category.query.get(upper_id)
            data.update({"module": upper.module, "level": 2, "upper_id": upper_id})
        else:
            data.update({"level": 1, "module": module})
        db.session.add(Category(**data))
        db.session.commit()

    def update(self, title, sort=20, upper_id=None):
        data = {"title": title, "sort": sort}

        if upper_id is None:
            data.update({"level": 1, "upper_id": None})
        elif upper_id != self.upper_id:
            upper = Category.query.get(Category.id == upper_id)
            if upper.module != self.module:
                return {"status": "failure", "msg": "不允许修改模块"}
            data.update({"level": 2, "upper_id": upper_id})
        self.set_attrs(data)
        db.session.commit()
        return {"stauts": "success", "msg": "修改成功"}

    def structure(self):
        return [self] if self.level == 1 else [self.upper, self]

