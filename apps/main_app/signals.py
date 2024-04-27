from django.db.models.signals import post_save
from django.dispatch import receiver
from background_task import background
from .models import UploadFileModel
from rest_framework.response import Response
from rest_framework import status
import shutil



@receiver(post_save, sender=UploadFileModel)
def copy_file_to_second_repository(sender, instance, created, **kwargs):
    if created:  
        original_file_path = instance.file.path
        new_file_path = "uploaded_files/second_repository/" + str(instance.file.name)

        try:
            shutil.copyfile(original_file_path, new_file_path)
            message ="The file was uploaded in second repository successfully"
            print(message)
            return Response({"message": message}, status=status.HTTP_201_CREATED)
        
        except Exception as error:
            message = f"An error occurred while copying file: {error}"
            print(message)
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
# @receiver(post_save, sender=UploadFileModel)
# def trigger_copy_file_to_second_repository(sender, instance, created, **kwargs):
#     if created:
#         copy_file_to_second_repository(instance.file.path, instance.file.name)

# @background(schedule=0)
# def copy_file_to_second_repository(original_file_path, new_file_name):
#     new_file_path = "uploaded_files/second_repository/" + str(new_file_name)

#     try:
#         shutil.copyfile(original_file_path, new_file_path)
#         message = "The file was uploaded in the second repository successfully"
#         print(message)
#     except Exception as error:
#         message = f"An error occurred while copying the file: {error}"
#         print(message)


   
