from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import FileResponse, HttpResponse, HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
import os
from custom_permission import *
from extra_services import * 
from .models import *
from .serializers import *


#======================================= File Upload =======================================
def worldwide_action(request):
    if not request.user.is_authenticated:
         request.session["display_name"]= "Guest"     
    else:
        if request.user.first_name != "" and request.user.last_name != "":
            request.session["display_name"]= f"{request.user.first_name} {request.user.last_name}" 
        else:
            request.session["display_name"]= request.user.email 
            

# def display_name(request):
#     if not request.user.is_authenticated:
#         return {'display_name': 'Guest'}
#     else:
#         if request.user.first_name and request.user.last_name:
#             return {'display_name': f'{request.user.first_name} {request.user.last_name}'}
#         else:
#             return {'display_name': request.user.email}


#=============================================================
class Upload_File_View(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    parser_classes = [MultiPartParser, FormParser]
    
    queryset = UploadFileModel.objects.all()
    serializer_class = UploadFileSerializer
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)
    
    
#=============================================================
class Delete_File_APIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [User_Check_Out]
    
    def delete(self, request, filename, format=None):
        uploaded_files = "uploaded_files/"
        user = f"{request.user.first_name}_{request.user.last_name}/"
        internal_folder = os.path.join(uploaded_files, user)
        file_path = os.path.join(media_root, internal_folder, filename)
        
        try:
            if os.path.exists(file_path):
                if self.check_object_permissions(request, file_path):
                    os.remove(file_path)
                    return Response({'message': 'File deleted successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'You are not allowed'}, status=status.HTTP_403_FORBIDDEN)
        
        except FileNotFoundError:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
  
  
#=============================================================
class Download_File_View(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [User_Check_Out]
    
    def get(self, request:Request, filename, format=None):
        uploaded_files = "uploaded_files/"
        user = f"{request.user.first_name}_{request.user.last_name}/"
        internal_folder = os.path.join(uploaded_files, user)
        file_path = os.path.join(media_root, internal_folder, filename)
        
        try:
            if os.path.exists(file_path):
                if self.check_object_permissions(request, file_path):
                    response = FileResponse(open(file_path, 'rb'))
                    return response
                else:
                    return Response({'error': 'You are not allowed'}, status=status.HTTP_403_FORBIDDEN)
            else:
                    return Response({'error': 'File Not exist any more'}, status=status.HTTP_404_NOT_FOUND)
                    
        except FileNotFoundError:
                return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)


#=============================================================
# class Upload_File_APIView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     parser_classes = [MultiPartParser, FormParser]

#     def post(self, request, format=None):
#         file = request.data.get('file')
#         metadata = request.data.get('metadata')
        
#         if file and metadata:
#             return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)


#=============================================================     
# def download_file_view(request, filename):
#     fs = FileSystemStorage()
#     file_name = str(filename)
#     uploaded_files = "uploaded_files/"
#     user = f"{request.user.first_name}_{request.user.last_name}/"
#     internal_folder = os.path.join(uploaded_files, user)
#     file_path = os.path.join(media_root, internal_folder, filename)
        
#     name, ext = os.path.split(file_name)
    
#     if ext == "txt":
#         return "text/plain"
    
#     elif ext == "docx":
#         return "application/msword"
    
#     elif ext == "pdf":
#         return "application/pdf"
    
#     if fs.exists(file_path):
#         with fs.open(file_path) as file_map:
#             # response = HttpResponse(file_map, content_type=f"application/{file_name.split('.')[-1]}")
#             response = HttpResponse(file_map, content_type=ext)
#             response["Content-Disposition"] = f"attachment; filename={file_name}"
#             return response
#     else:
#         return HttpResponseNotFound("File not found", status=status.HTTP_404_NOT_FOUND)


#=============================================================       


