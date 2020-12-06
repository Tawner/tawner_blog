from .marshmallows import *
from common.system.login_require import *
from flask.views import MethodView
from common.models import Article, db


# 前台接口
class ArticleListView(MethodView):
    """获取文章列表"""
    def get(self):
        req_val = ArticleListParse().load(request.values)

        articles = Article.list(**req_val, published=True)
        page_data = PaginateSchema().dump(articles)
        data = ArticleListSchema().dump(articles.items)
        return {"code": 200, "data": data, "page_data": page_data}


class ArticleInfoView(MethodView):
    """获取文章"""
    def get(self, article_id):
        article_obj = Article.query.filter(
            Article.id == article_id,
            Article.is_delete == 0,
            Article.published == True
        ).first()
        if not article_obj:
            abort(404, description="文章不存在")
        return {"code": 200, "data": ArticleInfoSchema().dump(article_obj)}


class ArticleTagListView(MethodView):
    """获取文章Tag列表"""
    def get(self):
        tags = Tag.query.filter_by(is_delete=0).order_by(Tag.sort.asc()).all()
        return {"code": 200, "data": ArticleTagListSchema().dump(tags)}


class TagArticleListView(MethodView):
    """Tag获取文章列表"""
    def get(self, tag_id):
        req_val = TagArticleListParse().load(request.values)
        tag = Tag.query.filter_by(id=tag_id, is_delete=0).first()
        if not tag:
            abort(404, description="这个标签不存在")
        result = tag.article_list(**req_val)
        articles = result.pop("items")
        tag_data = ArticleTagListSchema().dump(tag)
        tag_data['articles'] = ArticleInfoSchema().dump(articles)
        return {"code": 200, "page_data": result, "data": tag_data}


# 后台接口
class AddArticleView(MethodView):
    decorators = [admin_login_required]
    """添加文章"""
    def post(self):
        req_val = AddArticleParse().load(request.values)
        tag_ids = req_val.pop("tag_id", [])
        # 添加文章
        article_obj = Article(**req_val)
        db.session.add(article_obj)
        db.session.commit()
        # 添加标签
        article_tags = []
        for tag_id in tag_ids:
            article_tags.append(ArticleTag(article_id=article_obj.id, tag_id=tag_id))
        db.session.add_all(article_tags)
        db.session.commit()
        return {"code": 200, "msg": "添加成功"}


class ArticleInfoAdminView(MethodView):
    decorators = [admin_login_required]
    """获取、修改、删除文章"""
    def get(self, article_id):
        article_obj = Article.query.filter(Article.id == article_id, Article.is_delete == 0).first()
        if not article_obj:
            abort(404, description="文章不存在")
        return {"code": 200, "data": ArticleInfoAdminSchema().dump(article_obj)}

    def put(self, article_id):
        req_val = UpdateArticleInfo().load(request.values)
        article_obj = Article.query.filter(Article.id == article_id, Article.is_delete == 0).first()
        if not article_obj:
            abort(404, description="文章不存在")

        tag_ids = req_val.pop("tag_id", [])
        article_obj.set_attrs(req_val)
        # 删除旧tag
        delete_tag_id = [tag.id for tag in article_obj.tags]
        delete_tag = ArticleTag.query.filter(
            ArticleTag.article_id == article_obj.id,
            ArticleTag.tag_id.in_(delete_tag_id)
        ).all()
        for tag in delete_tag:
            db.session.delete(tag)
        # 添加新tag
        article_tags = []
        for tag_id in tag_ids:
            article_tags.append(ArticleTag(article_id=article_obj.id, tag_id=tag_id))
        db.session.add_all(article_tags)
        db.session.commit()
        return {"code": 200, "msg": "修改成功"}

    def delete(self, article_id):
        article_obj = Article.query.filter(Article.id == article_id, Article.is_delete == 0).first()
        if not article_obj:
            abort(404, description="文章不存在")
        tags = ArticleTag.query.filter(ArticleTag.article_id == article_id).all()
        for tag in tags:
            db.session.delete(tag)
        article_obj.delete()
        db.session.commit()
        return {"code": 200, "msg": "删除成功"}


class ArticleListAdminView(MethodView):
    decorators = [admin_login_required]
    """后台获取文章列表"""
    def get(self):
        req_val = ArticleListAdminParse().load(request.values)

        articles = Article.list(**req_val)
        page_data = PaginateSchema().dump(articles)
        data = ArticleListAdminSchema().dump(articles.items)
        return {"code": 200, "data": data, "page_data": page_data}


class TagListAdminView(MethodView):
    decorators = [admin_login_required]
    """获取tag列表"""

    def get(self):
        tags = Tag.query.filter_by(is_delete=0).order_by(Tag.sort.asc()).all()
        return {"code": 200, "data": TagListAdminSchema().dump(tags)}


class AddTagView(MethodView):
    decorators = [admin_login_required]
    """添加tag"""

    def post(self):
        req_val = AddTagParse().load(request.values)
        db.session.add(Tag(**req_val))
        db.session.commit()
        return {"code": 200, "msg": "添加成功"}


class TagInfoAdminView(MethodView):
    decorators = [admin_login_required]
    """修改、删除tag"""

    def put(self, tag_id):
        req_val = UpdateTagInfoParse().load(request.values)
        tag = Tag.query.filter_by(id=tag_id, is_delete=0).first()
        if not tag:
            abort(404, description="这个标签不存在")
        tag.set_attrs(req_val)
        db.session.commit()
        return {"code": 200, "msg": "修改成功"}

    def delete(self, tag_id):
        tag = Tag.query.filter_by(id=tag_id, is_delete=0).first()
        if not tag:
            abort(404, description="这个标签不存在")
        tags = ArticleTag.query.filter_by(tag_id=tag.id).all()
        for tag in tags:
            db.session.delete(tag)
        tag.delete()
        db.session.commit()
        return {"code": 200, "msg": "删除成功"}



