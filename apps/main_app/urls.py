from django.urls import path,re_path
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register("upload-files", Upload_File_View)

app_name = "Main_App"
urlpatterns = [
    path("delete-file/<str:filename>/",Delete_File_APIView.as_view(),name="Delete_File"),
    path("download-file/<str:filename>/",Download_File_View.as_view(),name="Download_File"),
    # path("upload-file/",Upload_File_APIView.as_view(),name="Upload_File"),
    # path("download-file/<str:filename>/", download_file_view, name="Download_File"),
]

urlpatterns += router.urls