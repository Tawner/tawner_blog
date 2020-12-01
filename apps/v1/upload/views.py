from common.models import Upload
from flask.views import MethodView
from flask import Blueprint, request, abort
from common.utility import *
import os
from datetime import datetime

upload_bp = Blueprint('upload', __name__)


class UploadView(MethodView):

    def post(self):
        file = request.files.get('file', None)
        result = Upload.save_file(file)

        if result['status'] == "failure":
            abort(400, description=result['msg'])
        return {"code": 200, "data": {"id": result['id'], "url": result['url']}}


class EditorUploadView(MethodView):

    def post(self):
        file = request.files.get('file', None)

        if not file:
            abort(400, description="没有上传文件")
        filename, file_type = os.path.splitext(file.filename)
        if file_type[1:] not in current_app.config['ALLOWED_EXTENSIONS']:
            abort(400, description="不允许上传的文件类型")
        if len(file.read()) > current_app.config['MAX_CONTENT_LENGTH']:
            abort(400, description="上传的文件大小超出限制")

        filename = '/%s_%s%s' % (filename, datetime.now().strftime('%y%m%d%H%M%S'), file_type)
        save_path = current_app.config['EDITOR_UPLOAD_FOLDER'] + filename
        file.seek(0)
        file.save(save_path)
        return {"code": 200, "url": current_app.config['WEB_HOST_NAME'] + 'api/uploads/editor/' + filename}
