from rest_framework.permissions import BasePermission, SAFE_METHODS  
from rest_framework.request import Request


class User_Check_Out(BasePermission):
	message = "You are not allowed"

	def has_permission(self, request: Request, obj=None):
		return request.user and request.user.is_authenticated

	def has_object_permission(self, request: Request, view, obj):
		if request.method in SAFE_METHODS:
			return True
		return obj.user == request.user
