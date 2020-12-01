from flask import Blueprint
from . import article, upload, category, admin, site, user


def blue_print():
    """创建蓝图，注册路由"""
    api_v1_bp = Blueprint("api_v1", __name__)
    # 注册url
    admin.add_url_rule(api_v1_bp)
    article.add_url_rule(api_v1_bp)
    upload.add_url_rule(api_v1_bp)
    category.add_url_rule(api_v1_bp)
    site.add_url_rule(api_v1_bp)
    user.add_url_rule(api_v1_bp)
    return api_v1_bp




