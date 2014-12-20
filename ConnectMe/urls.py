from django.conf.urls import patterns, url, include
# from ConnectMeApp import views
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	
    # Core Routes
#     url('^login/$', TemplateView.as_view(template_name='login.html')),
    url('^signup/$', TemplateView.as_view(template_name='signup.html')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'ConnectMeApp.views.home', name='home'),
	url(r'^api/event/createEvent/$', name='createEvent'),
	url(r'^api/event/leaveEvent/$', name='leaveEvent'),
	url(r'^api/event/deleteEvent/$', name='deleteEvent'),
	url(r'^api/event/sendInvite/$', name='sendInvite'),
	url(r'^api/event/joinEvent/$', name='joinEvent'),
	url(r'^api/event/friendevents/(?P<user_id>[\w]{24})$', name='friendEvents'),
	url(r'^api/event/publicevents/$', name='publicEvents'),
	url(r'^api/calendar/getattendingevents/$', name='getAttendingEvents'),
	url(r'^api/calendar/getinvitedevents/$', name='getInvitedEvents'),
	
#  	url('listf', 'ConnectMeApp.views.Getfriends'),
#  	url(r'^accounts/', include('allauth.urls')),
	
	#url(r'^$', 'socialauth.views.signin_complete'),
	#url(r'^$', TemplateView.as_view(template_name='home.html')),
	
    # GET
    #url(r'^api/users/$', views.UserList.as_view()),
    
	# POST
   # url(r'^api/login/$', views.Login.as_view()),
    
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
   
    url(r'', include('jqmobile.urls'))
)
