from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser

#======================================= Users =======================================

class CustomUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=20,write_only=True)
    
    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {
            "password":{"write_only":True}
        } 
        
    def create(self,validated_data):
        del validated_data["re_password"]
        return CustomUser.objects.create(**validated_data)
        
    def validate(self,data):
        if data["password"] != data["re_password"]:
            raise serializers.ValidationError("The password and re_password do not match")
            
        try:
            validate_password(data["password"])
        except ValidationError as error:
            raise serializers.ValidationError(str(error))
            
        return data
 

#====================================================
    
class VerifyingEmailSerializer(serializers.Serializer):
    activation_code=serializers.CharField(max_length=10)


#====================================================

class LoginUserSerializer(serializers.Serializer):
    email=serializers.CharField(max_length=40)
    password=serializers.CharField(max_length=20)
    
    # data_to_validate = {}
    
#====================================================   

class ChangingPasswordSerializer(serializers.Serializer):   
    password=serializers.CharField(max_length=20)
    re_password=serializers.CharField(max_length=20)
    
    def validate(self,data):
        if data["password"] != data["re_password"]:
            raise serializers.ValidationError("The password and re_password do not match")
            
        try:
            validate_password(data["password"])
        except ValidationError as error:
            raise serializers.ValidationError(str(error))
        return data
    
    
#====================================================
    
class RememberPasswordSerializer(serializers.Serializer):
    email=serializers.CharField(max_length=40)
    
    
#====================================================

class Update_Profile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id","first_name","last_name","email"]
        
        
    def create(self,validated_data):
        return CustomUser.objects.create(**validated_data)
    
#====================================================
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             

             
             
             
             
             
             
             
             
             
             
             
             
             
             
