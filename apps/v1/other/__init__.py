from .views import *


def add_url_rule(api_bp):
    api_bp.add_url_rule('/lol_skin', view_func=LolSkinView.as_view('lol_skin'))
