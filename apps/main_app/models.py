from django.db import models
from apps.accounting.models import CustomUser
from django.core.validators import FileExtensionValidator, MaxValueValidator
from extra_services import *


class UploadFileModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="User")
    file = models.FileField(upload_to=upload_to, validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt']),  
            MaxValueValidator(5242880)  # Restrict file size to 5MB (in bytes)
        ], verbose_name="File")
    metadata = models.JSONField(blank=True, null=True, verbose_name="Metadata")  # Additional metadata field
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Uploaded At")
    
    def __str__(self):
        return f"{self.user.email} - {self.file.name}"
