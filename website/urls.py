from django.urls import path

from .views import (
    home,
    upload_file,
    protected_file,
    download_file,
    dashboard,
)


urlpatterns = [
    path("", home, name="home"),

    path(
        "upload/",
        upload_file,
        name="upload_file"
    ),

    path(
        "file/<int:file_id>/",
        protected_file,
        name="protected_file"
    ),

    path(
        "file/<int:file_id>/download/",
        download_file,
        name="download_file"
    ),

    path(
        "dashboard/",
        dashboard,
        name="dashboard"
    ),
]