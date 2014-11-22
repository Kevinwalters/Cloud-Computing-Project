from django.conf.urls import patterns, url
from obo import views
from django.views.generic import TemplateView

# Import Controllers
#from obo.UserController import UserController
#from obo.EventController import EventController
#from obo.SubscriptionController import SubscriptionController

# Import system
# from System import System

# TODO
#
# 1. Differentiate between GET, POST, PUT, DELETE 
# 2. Get data from POST request

urlpatterns = patterns('',
	
    # Core Routes
    url('^login/$', TemplateView.as_view(template_name='login.html')),
    url('^signup/$', TemplateView.as_view(template_name='signup.html')),

    # GET
    url(r'^api/users/$', views.UserList.as_view()),
)
