from django.contrib import admin
from .models import *


@admin.register(UploadFileModel)
class UploadFileAdmin(admin.ModelAdmin):
    list_display = ("user","file","metadata","uploaded_at",)
    list_filter = ("file",)
    search_fields = ("logged_user",)
    ordering = ("file",)