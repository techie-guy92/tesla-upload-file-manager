from django.urls import path,re_path
from rest_framework.routers import DefaultRouter 
from .views import *


router = DefaultRouter()
router.register("update",Update_Delete_User_View)


app_name="Accounting"
urlpatterns = [
    path("register/",RegisterUserView.as_view(),name="register"),
    path("verify-email/",VerifyingEmailView.as_view(),name="verify-email"),
    path("login/",LoginUserView.as_view(),name="login"),
    path("logout/",LogoutUserView.as_view(),name="logout"),
    path("change-pass/",ChangingPasswordView.as_view(),name="change-pass"),
    path("remember-pass/",RememberPasswordView.as_view(),name="remember-pass"),
]

urlpatterns += router.urls

