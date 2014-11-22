from rest_framework_mongoengine.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *
from UserController import UserController
#from CalendarController import CalendarController
from django.http.response import HttpResponse
from rest_framework.response import Response
from django.shortcuts import render_to_response
from django.template.context import RequestContext

class UserList(ListCreateAPIView):
	print "GET /api/users"
	serializer_class = UserSerializer
	queryset = User.objects.all()