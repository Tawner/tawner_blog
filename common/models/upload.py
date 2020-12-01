from .base import Base, db
from common.utility import *
from flask import current_app
import os


class Upload(Base):
    __tablename__ = 'upload'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(252), comment='文件名')
    file_md5 = db.Column(db.String(128), comment='文件md5')
    file_type = db.Column(db.SmallInteger, default=0, comment='文件类型')  # 0 图片 1 文件
    file_size = db.Column(db.Integer, default=0, comment='文件大小')
    path = db.Column(db.String(256), comment='文件路径')

    @property
    def url(self):
        path = self.path.split('uploads/')[-1]
        url = current_app.config['WEB_HOST_NAME'] + 'api/uploads/' + path
        return url

    @classmethod
    def save_file(cls, file):
        if not file: return {'status': "failure", "msg": "没有上传文件"}

        filename, file_type = os.path.splitext(file.filename)
        if file_type[1:] in current_app.config['ALLOWED_IMAGE']: upload_type = 0
        elif file_type[1:] in current_app.config['ALLOWED_file']: upload_type = 1
        else: return {"status": "failure", "msg": "不允许上传的文件类型"}

        if len(file.read()) > current_app.config['MAX_CONTENT_LENGTH']:
            return {"status": "failure", "msg": "上传的文件大小超出限制"}

        md5_code = md5(file.read())
        upload_file = Upload.query.filter(Upload.file_md5 == md5_code).first()
        if upload_file:
            return {"status": "success", "url": upload_file.url, 'id': upload_file.id}
        else:
            r_path = current_app.config['UPLOAD_FOLDER'] + 'file/' if upload_file else 'image/' + md5_code + file_type,
            inset_data = {
                "filename": filename,
                "file_md5": md5_code,
                "file_type": upload_type,
                "file_size": len(file.read()),
                "path": r_path
            }
            upload_file = Upload(**inset_data)
            file.seek(0)
            file.save(r_path)
            db.session.add(upload_file)
            db.session.commit()
            return {"status": "success", "url": upload_file.url, 'id': upload_file.id}