"""
URL configuration for upload_file_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from rest_framework.authtoken import views
from extra_services import * 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')), #login or log out
    path('api-token-auth/',views.obtain_auth_token),
    path('accounting/',include("apps.accounting.urls",namespace="Accounting")),
    path('',include("apps.main_app.urls",namespace="Main_App")),
]


urlpatterns += static(media_url,document_root=media_root)

# if settings.DEBUG:
#     urlpatterns += static(media_url,document_root=media_root)


# admin.site.site_title = ""
admin.site.site_header= "Administration Panel"
# admin.site.index_title= ""
# handler404 = ""



