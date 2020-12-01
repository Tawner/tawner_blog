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
        ).frist()
        if not article_obj:
            abort(404, description="文章不存在")
        return {"code": 200, "data": ArticleInfoSchema().dump(article_obj)}


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
        article_obj = Article.query.filter(Article.id == article_id, Article.is_delete == 0).frist()
        if not article_obj:
            abort(404, description="文章不存在")
        return {"code": 200, "data": ArticleInfoAdminSchema().dump(article_obj)}

    def put(self, article_id):
        req_val = UpdateArticleInfo().load(request.values)
        article_obj = Article.query.filter(Article.id == article_id, Article.is_delete == 0).frist()
        if not article_obj:
            abort(404, description="文章不存在")

        tag_ids = req_val.pop("tag_id", [])
        article_obj.set_attrs(req_val)
        # 删除旧tag
        for tag in article_obj.tags:
            if tag.id not in tag_ids:
                db.session.delete(tag)
            else:
                tag_ids.pop(tag.id)
        # 添加新tag
        article_tags = []
        for tag_id in tag_ids:
            article_tags.append(ArticleTag(article_id=article_obj.id, tag_id=tag_id))
        db.session.add_all(article_tags)
        db.session.commit()
        return {"code": 200, "msg": "修改成功"}

    def delete(self, article_id):
        article_obj = Article.query.filter(Article.id == article_id, Article.is_delete == 0).frist()
        if not article_obj:
            abort(404, description="文章不存在")

        ArticleTag.query.filter(ArticleTag.article_id == article_id).update({"is_delete": 1})
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

