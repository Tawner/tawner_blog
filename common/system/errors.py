from flask import jsonify, current_app
from werkzeug.http import HTTP_STATUS_CODES
from marshmallow.exceptions import ValidationError


# response构建
def api_abort(code, message=None):
    if message is None:
        message = HTTP_STATUS_CODES.get(code, '')

    response = jsonify(code=code, message=message)
    return response, code


# 异常捕获
def error_handler(app):

    @app.errorhandler(400)
    def bad_request(e):
        return api_abort(400, e.description)

    @app.errorhandler(403)
    def forbidden(e):
        return api_abort(403, e.description)

    @app.errorhandler(404)
    def database_not_found_error_handler(e):
        return api_abort(404, e.description)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return api_abort(405, e.description)

    @app.errorhandler(500)
    def internal_server_error(e):
        return api_abort(500, e.description)
    
    @app.errorhandler(ValidationError)
    def param_error(e):
        return api_abort(400, e.description)

    @app.errorhandler(Exception)
    def default_error_handler(e):
        message = 'An unhandled exception occurred. -> {}'.format(str(e))
        current_app.logger.error(message)
        if not current_app.config["DEBUG"]:
            return api_abort(500, "服务器发生了一个意料之外的错误")


def invalid_token():
    response, code = api_abort(401)
    return response, code


# class ValidationError(ValueError):
#     pass

# 简单列了一些，别的类型自己可以根据需要扩展补充
# from itpms.api.v1.order import api as order_api
# @order_api.errorhandler(ValidationError)
# def validation_error(e):
#     return api_abort(400, e.args[0])



