from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseForbidden
from .models import *
from .forms import *


#======================================= Users =======================================

class CreatingAdminUserAdmin(UserAdmin):
    
    add_form=CreatingAdminUserForm
    form=EditAdminUserForm
    
    
    list_display=("id","first_name","last_name","email","gender","is_active","is_admin","is_superuser",)
    list_filter=("is_superuser","is_admin","is_active","gender",)
    
    
    add_fieldsets=(
        ("User information",{"fields":("email","password","re_password",)}),
        ("Personal information",{"fields":("first_name","last_name","gender",)}),
    )
    
    fieldsets=(
        ("User information",{"fields":("email","password",)}),
        ("Personal information",{"fields":("first_name","last_name","gender",)}),
        ("Accessibilities",{"fields":("is_active","is_admin","is_superuser","groups","user_permissions",)}),
    )
    
    list_editable = ("is_admin","is_active",)
    sreach_fields = ("email",)
    ordering = ("is_superuser","is_admin","is_active","last_name","first_name",)
    filter_horizontal = ("groups","user_permissions",)

    def change_view(self, request, object_id, form_url='', extra_context=None):
         
        if CustomUser.objects.filter(pk=object_id, is_superuser=True).exists() and request.user.is_superuser is False: 
            return HttpResponseForbidden('<h1 style="color:red; text-align:center;">You are not allowed to see this page</h1>') 
        if CustomUser.objects.filter(pk=object_id, is_admin=True).exists() and request.user.is_superuser is False: 
            return HttpResponseForbidden('<h1 style="color:red; text-align:center;">You are not allowed to see this page</h1>') 
        if CustomUser.objects.filter(pk=object_id, is_superuser=True).exists() and request.user.is_superuser is True: 
            return HttpResponseForbidden('<h1 style="color:black; text-align:center;">You are not allowed to see this page</h1>') 
         
        return super().change_view(request, object_id, form_url, extra_context)


admin.site.register(CustomUser,CreatingAdminUserAdmin)


