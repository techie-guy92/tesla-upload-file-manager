from django import forms 
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *


#======================================= Users Admin =======================================
class CreatingAdminUserForm(forms.ModelForm):
    password=forms.CharField(label="Password",widget=forms.PasswordInput)
    re_password=forms.CharField(label="Re_password",widget=forms.PasswordInput)
    
    class Meta:
        model=CustomUser
        fields=["first_name","last_name","email","gender"]
        
        
    def clean_re_password(self):
        pass1=self.cleaned_data["password"]
        pass2=self.cleaned_data["re_password"]
        
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("The password and re_password do not match")
        return pass2
    
    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
    
#====================================================   
class EditAdminUserForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField(help_text="Click on <a href='../password'>link</a> to change your password")
    
    # password = ReadOnlyPasswordHashField(
    #     label=("Password"),
    #     help_text=(
    #         "Click on <a href='../password'>link</a> to change your password"
    #     ),)
    
    class Meta:
        model=CustomUser
        fields=["email","password","is_active",]
        # fields=["email","password","is_active","is_admin"]
 
            
#======================================= Users =======================================
class RegisterUserForm(ModelForm):
    password= forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password'}))
    re_password= forms.CharField(label="Re_password",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your re_password'}))
    
    class Meta:
        model=CustomUser
        fields=["email",]
        widgets={"email": forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your email'})}
 
    def clean_re_password(self):
        pass1= self.cleaned_data["password"]
        pass2= self.cleaned_data["re_password"]
        
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("The password and re_password do not match")
        return pass2
    

#====================================================
class VerifyingCellNumberForm(forms.Form):
    activation_code=forms.CharField(label="Activation Code",
                                    error_messages={"required":"The activation code must be entered"},
                                    widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your activation code'}))


#====================================================
class LoginUserForm(forms.Form):
    email=forms.CharField(label="Email",
                                    error_messages={"required":"The email must be entered"},
                                    widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your email'}))
    
    password=forms.CharField(label="Password",
                                    error_messages={"required":"The password must be entered"},
                                    widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password'}))
    
    
#====================================================   
class ChangingPasswordForm(forms.Form):   
    password=forms.CharField(label="Password",
                                    error_messages={"required":"The password must be entered"},
                                    widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password'}))
    
    re_password=forms.CharField(label="Re_password",
                                    error_messages={"required":"The re_password must be entered"},
                                    widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your re_password'}))
    
    def clean_re_password(self):
        pass1=self.cleaned_data["password"]
        pass2=self.cleaned_data["re_password"]
        
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("The password and re_password do not match")
        return pass2
    
    
#====================================================
class RememberPasswordForm(forms.Form):
    email=forms.CharField(label="Email",
                                    error_messages={"required":"The email must be entered"},
                                    widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your email'}))
    
    
#====================================================
class Update_Profile_Form(forms.Form):
    
    first_name=forms.CharField(label="First Name",
                                    error_messages={"required":"The first name must be entered"},
                                    widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your first name'}))
    
    last_name=forms.CharField(label="Last Name",
                                    error_messages={"required":"The last name must be entered"},
                                    widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your last name'}))
    
    email=forms.EmailField(label="Email",
                                    error_messages={"required":"The email must be entered"},
                                    widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your email'}))
    
    image=forms.ImageField(label="Picture",
                           required=False)
    

    
#====================================================
    
    
    
    
    