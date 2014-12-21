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
	url(r'^api/event/createevent/$', 'ConnectMeApp.views.createEvent',name='createEvent'), #WORKS
	url(r'^api/event/leaveevent/$', 'ConnectMeApp.views.leaveEvent',name='leaveEvent'), #WORKS
	url(r'^api/event/deleteevent/$', 'ConnectMeApp.views.deleteEvent',name='deleteEvent'), #WORKS
	url(r'^api/event/sendinvite/$', 'ConnectMeApp.views.sendInvite',name='sendInvite'), #WORKS
	url(r'^api/event/joinevent/$', 'ConnectMeApp.views.joinEvent',name='joinEvent'), #WORKS
	url(r'^api/event/friendevents/(?P<user_id>[\w]{24})/$', 'ConnectMeApp.views.friendEvents',name='friendEvents'), #WORKS
	url(r'^api/event/publicevents/$', 'ConnectMeApp.views.publicEvents', name='publicEvents'), #WORKS(NOT TESTED WITH DATA - SITE DOWN)
	url(r'^api/calendar/getattendingevents/$', 'ConnectMeApp.views.getAttendingEvents',name='getAttendingEvents'),
	url(r'^api/calendar/getinvitedevents/$', 'ConnectMeApp.views.getInvitedEvents',name='getInvitedEvents'),
	
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
   
    # url(r'', include('jqmobile.urls'))
)
