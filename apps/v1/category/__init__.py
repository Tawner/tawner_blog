from .views import *


def add_url_rule(api_bp):
    api_bp.add_url_rule('/category/list', view_func=CategoryListView.as_view('category_list'))
    api_bp.add_url_rule('/admin/category', view_func=AddCategoryView.as_view('add_category'))
    api_bp.add_url_rule('/admin/category/<int:category_i>', view_func=CategoryView.as_view('category_info'))
    api_bp.add_url_rule('/admin/category/list', view_func=CategoryListAdminView.as_view('admin_category_list'))




