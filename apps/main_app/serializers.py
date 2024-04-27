from rest_framework import serializers
from .models import UploadFileModel

    
class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFileModel
        fields = "__all__"  
       
    def validate(self, data):
        file = data.get("file")
        metadata = data.get("metadata")
        if not file:
            raise serializers.ValidationError("The uploaded file cannot be empty")
        return data

    def create(self, validated_data):
        return UploadFileModel.objects.create(**validated_data)