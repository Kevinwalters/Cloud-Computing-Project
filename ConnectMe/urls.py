from django.conf.urls import patterns, url
from ConnectMe import views
from django.views.generic import TemplateView

urlpatterns = patterns('',
	
    # Core Routes
    url('^login/$', TemplateView.as_view(template_name='login.html')),
    url('^signup/$', TemplateView.as_view(template_name='signup.html')),

    # GET
    url(r'^api/users/$', views.UserList.as_view()),
)
