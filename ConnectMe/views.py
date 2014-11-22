from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from rest_framework.response import Response
from rest_framework_mongoengine.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from UserController import UserController

from .serializers import *


#from CalendarController import CalendarController
class UserList(ListCreateAPIView):
	print "GET /api/users"
	serializer_class = UserSerializer
	queryset = User.objects.all()
	
class Login(RetrieveUpdateDestroyAPIView):
	serializer_class = UserSerializer
	queryset = User.objects.all()

	def post(self, request):
		print "POST /api/login"
		email = request.DATA['email']
		password = request.DATA['password']
		
		user_id = UserController.login(email, password)

		print user_id
		if not user_id:
			return Response(401)
		return HttpResponse(user_id)