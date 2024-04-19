# Generated by Django 5.0.4 on 2024-04-18 10:32

import django.core.validators
import extra_services
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_uploadfilemodel_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfilemodel',
            name='file',
            field=models.FileField(upload_to=extra_services.Uploading_Files.file_name, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt']), django.core.validators.MaxValueValidator(5242880)], verbose_name='File'),
        ),
    ]
