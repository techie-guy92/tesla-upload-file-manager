from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from extra_services import *


#======================================= Users =======================================
class CustomUserManager(BaseUserManager):
    
    def create_user(self,email,first_name,last_name,image=None,gender=None,activation_code=None,password=None):
        
        if not email:
            raise ValueError("The Email field must be set")
        
        user=self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            activation_code=activation_code,
            gender=gender or "no-gender",
            image=image or "images/no-photo.jpg",
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,first_name,last_name,image=None,gender=None,activation_code=None,password=None):
        
        user=self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            activation_code=activation_code,
            gender=gender or "no-gender" ,
            image=image or "images/no-photo.jpg",
            password=password,
        )
        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
    
   
#====================================================================================
class CustomUser(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=50,verbose_name="First Name")
    last_name = models.CharField(max_length=50,verbose_name="Last Name")
    email = models.EmailField(unique=True,verbose_name="Email")
    gender_optins = (("no-gender","Rather not to say"),("male","Male"),("female","Female"))
    gender = models.CharField(max_length=50,choices=gender_optins,default="no-gender",blank=True,null=True,verbose_name="Gender")
    folder_path = Uploading_Files("images","users")
    image = models.ImageField(upload_to=folder_path.file_name,blank=True,default="images/no-photo.jpg",verbose_name="Image")
    created_at = models.DateTimeField(default=timezone.now)
    activation_code = models.CharField(max_length=20,blank=True,null=True,verbose_name="Activation Code")
    is_active= models.BooleanField(default=False,verbose_name="Being Active")
    is_admin = models.BooleanField(default=False,verbose_name="Being Staff")
    is_superuser = models.BooleanField(default=False,verbose_name="Being Superuser")
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name",]
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}  {self.email}  {self.gender}"

    class Meta:
      verbose_name = "User"
      verbose_name_plural = "Users"

    @property
    def is_staff(self):
        return self.is_admin
    

#===============================================================================================================================






