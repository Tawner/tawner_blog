from .views import *


def add_url_rule(api_bp):
    api_bp.add_url_rule('/download/list', view_func=DownloadListView.as_view('download_list'))
    api_bp.add_url_rule('/download/<int:download_id>', view_func=DownloadFileView.as_view('download_file'))
    api_bp.add_url_rule('/admin/download/list', view_func=DownloadListAdminView.as_view('admin_download_list'))
    api_bp.add_url_rule('/admin/download', view_func=AddDownloadView.as_view('admin_add_download'))
    api_bp.add_url_rule('/admin/download/<int:download_id>', view_func=DownloadInfoView.as_view('admin_download_info'))
