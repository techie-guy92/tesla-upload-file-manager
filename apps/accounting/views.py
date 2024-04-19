from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import *
from rest_framework.views import APIView
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.request import Request
from extra_services import *
from datetime import datetime
from extra_services import *
from .models import CustomUser
from .serializers import *
from .forms import *

#======================================= Upload File Manager =======================================
class RegisterUserView(APIView):
    
    def get(self, request: Request, Request,):
        serializer = CustomUserSerializer()
        return Response(data=serializer.data)
    
    def post(self, request: Request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
        # if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            activation_code = generating_random_code(5)
            CustomUser.objects.create_user(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                password=data["password"],
                activation_code=activation_code,
            )
            passed_time = str(timezone.now())

            subject = "Registration"
            message = f"<h4>Hello Dear {data.get('first_name')} {data.get('last_name')}<br><br><h4>Your activation code is : {activation_code}</h4>"
            to = data.get('email')
            Sending_Mail(subject, "", message, [to])
            
            request.session["user_session"] = {
                "activation_code":str(activation_code),
                "email":data.get('email'),
                "passed_time":passed_time,
                "remember_pass_status":False,
                }
            
            return Response({"message": "Your information has logged, to complete your registration enter your validation code"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        
#====================================================
class VerifyingEmailView(APIView):

    def get(self, request: Request, *args, **kwargs):
        serializer = VerifyingEmailSerializer()
        return Response(data=serializer.data)

    def post(self, request: Request, *args, **kwargs):
        serializer = VerifyingEmailSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            user_session = request.session["user_session"]
            user_db= CustomUser.objects.get(email=user_session["email"])
            # passed_time_2 = user_session["passed_time"]
            # passed_time_3 = datetime.strptime(passed_time_2,"%Y-%m-%d %H:%M:%S.%f")
            # time_diff = timezone.now() - passed_time_3
            # total_seconds = time_diff.total_seconds()
            
            # if total_seconds <= 120:
                  
            if data.get("activation_code") == user_session["activation_code"]:
                    
                    if user_session["remember_pass_status"] == False:
                        user_db.is_active = True
                        user_db.activation_code = generating_random_code(5)
                        user_db.save()
                        return Response({"message": "Registration has been completed successfully"}, status=status.HTTP_201_CREATED)
                    
                    else:
                        return Response(status=status.HTTP_202_ACCEPTED, headers={"Location": "/change_pass/"})
                    
            else:
                return Response({"message":"Validation code is wrong"}, status=status.HTTP_406_NOT_ACCEPTABLE) 
                
            # else:
            #     activation_code = generating_random_code(5)
            #     user_db.activation_code = activation_code
            #     user_db.save()
            #     return Response({"message":"Validation code is expired"}, status=status.HTTP_410_GONE)
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
#====================================================
class LoginUserView(APIView):

    def get(self, request: Request, *args, **kwargs):
        serializer = LoginUserSerializer()
        return Response(data=serializer.data)

    def post(self, request: Request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data.get("email")
            password = request.data.get("password")
            user_auth = authenticate(username=username, password=password)
            if user_auth is not None:
                login(request, user_auth)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


#====================================================
class LogoutUserView(APIView):
    
    def get(self, request: Request, *args, **kwargs):
        logout(request)
        return Response({'message': 'Logout'})

#====================================================
class ChangingPasswordView(APIView):

    def get(self, request: Request, *args, **kwargs):
        serializer = ChangingPasswordSerializer()
        return Response(data=serializer.data) 


    def post(self, request: Request, *args, **kwargs):
        serializer = ChangingPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            user_session=request.session["user_session"]
            user = CustomUser.objects.get(email=user_session["email"])
            user.set_password(data["password"])
            user.activation_code = generating_random_code(5)
            user.save()
            return Response({"message":"Password has been changed successfully"},status=status.HTTP_202_ACCEPTED,header={"Location":"/login/"})
        return Response({"message":"Validation code is wrong"},status=status.HTTP_406_NOT_ACCEPTABLE)
            
    
#====================================================
class RememberPasswordView(APIView):
    
    def get(self, request: Request, *args, **kwargs):
        serializer = RememberPasswordSerializer()
        return Response(data=serializer.data) 
    
    def post(self, request: Request, *args, **kwargs):
        serializer = RememberPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                user = CustomUser.objects.get(email=data["email"])
                activation_code = generating_random_code(5)
                user.activation_code = activation_code
                user.save()
                
                subject = "Password recovery"
                message = f"<h4>Hello<br><br><h4>Your activation code is : {activation_code}</h4>"
                to = user
                Sending_Mail(subject,"",message,to)
                passed_time = str(timezone.now())
                
                request.session["user_session"]= {
                    "activation_code":str(activation_code),
                    "email":data["email"],
                    "passed_time":passed_time,
                    "remember_pass_status":True,
                }
                return Response({"message":"Enter your validation code"},status=status.HTTP_202_ACCEPTED, headers={"Location":"/verify_email/"})
            
            except:
                return Response({"message":"Email is wrong"},status=status.HTTP_410_GONE) 


#====================================================
class Update_Delete_User_View(LoginRequiredMixin,viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = Update_Profile_Serializer
    

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
       
    def update(self, request, *args, **kwargs):
        obj = super().update(request, *args, **kwargs)
        instance = self.get_object()
        print(f"{obj} {instance.first_name} {instance.last_name}")
        return obj
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)  
    
#===================================================================================
