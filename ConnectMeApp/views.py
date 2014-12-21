from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template.context import RequestContext
from rest_framework.response import Response
# from rest_framework_mongoengine.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ConnectMeApp import UserController
import urllib2
import json
from django.shortcuts import redirect
from decorators import render_to
from EventController import EventController
from CalendarController import CalendarController

UserController=UserController

def leaveEvent(request):
    print "==========LEAVE EVENT=========="
    result = EventController.leaveEvent(request.POST['user_id'], request.POST['event_id'])
    if result == "fail":
        return HttpResponse("Fail", status=401)
    else:
        return HttpResponse("Success")

def createEvent(request):
    print "==========CREATE EVENT=========="
    invite_list = json.loads(request.POST['invite_list'])
    tags = json.loads(request.POST['tags'])
    result = EventController.createEvent(request.POST['user_id'], request.POST['name'], request.POST['description'], request.POST['location'], request.POST['date'], request.POST['start_time'], request.POST['end_time'], tags, request.POST['is_private'], invite_list)
    if result == "fail":
        return HttpResponse("Fail", status=401)
    else:
        return HttpResponse("Success")
        
def deleteEvent(request):
    print "==========DELETE EVENT=========="
    result = EventController.deleteEvent(request.POST['event_id'])
    if result == "fail":
        return HttpResponse("Fail", status=401)
    return HttpResponse("Success")
        
def sendInvite(request):
    print "==========SEND INVITE=========="
    result = EventController.sendInvite(request.POST['event_id'], request.POST['user_id'])
    if result == "fail":
        return HttpResponse("Fail", status=401)
    else:
        return HttpResponse("Success")

def joinEvent(request):
    print "==========JOIN EVENT=========="
    result = EventController.joinEvent(request.POST["user_id"], request.POST["event_id"])
    if result == "fail":
        return HttpResponse("Fail", status=401)
    else:
        return HttpResponse("Success")
        
def friendEvents(request, user_id):
    print "==========GET ALL FRIENDS=========="
    friendEvents = EventController.getFriendEvents(user_id)#may need to do request.DATA['user_id']
    if friendEvents == "fail":
        return HttpResponse("Fail", status=401)
    else:
        return HttpResponse(friendEvents)
        
def publicEvents(request):
    print "==========PUBLIC EVENTS=========="
    publicEvents = EventController.getPublicEvents()
    if publicEvents == "fail":
        return HttpResponse("Fail", status=401)
    else:
        return HttpResponse(publicEvents)
        
def getAttendingEvents(request):
    attendingEvents = CalendarController.getAttendingEvents(request.user_id)
    if not attendingEvents or attendingEvents == "fail":
        HttpResponse("Fail", status=401)
    else:
        HttpResponse(attendingEvents)
        
def getInvitedEvents(request):
    invitedEvents = CalendarController.getInvitedEvents(request.user_id)
    if not invitedEvents or invitedEvents == "fail":
        HttpResponse("Fail", status=401)
    else:
        HttpResponse(invitedEvents)
    
  
def home(request):
#     
    if request.user.is_authenticated():
        print request.user
        context = RequestContext(request,
                                {'request': request,
                                 'user': request.user})
                  
        return render_to_response('login.html',Getfriends(request),
                                  context_instance=context)
    else:
        context = RequestContext(request,
                                {'request': request,
                                 'user': request.user})
        return render_to_response('home.html',
                                  context_instance=context)
  
             

# @login_required
# @render_to('home.html')   
def Getfriends(request):
    print 'haha?'
    if request.user.is_authenticated():
                print 'haha??'         
                print request.user.social_auth  
                if hasattr(request.user, 'social_auth'):
      #              print 'haha???'
                    social_user = request.user.social_auth.filter(provider='facebook')
#                     social_user = social_user.order_by('-id')
                    print social_user
                    #print social_user.extra_data
                    
                
    else : print 'not logged in'
    if social_user:# for friend in social_user:
        for usr in social_user:
            url = u'https://graph.facebook.com/{0}/' \
                u'friends?fields=id,name,location,picture' \
                u'&access_token={1}'.format(usr.uid, usr.extra_data['access_token'],)
            request = urllib2.Request(url)
            friends = json.loads(urllib2.urlopen(request).read()).get('data')
        #print friends
            print friends
            for friend in friends:
                print friend


    HttpResponse('ok!')
        
            
        
    # ...
     
#     def get_context_data(self, **kwargs):
#         context = super(FlightDetail, self).get_context_data(**kwargs)
#         friends_in_city = []
#         
#             if social_user:
#                 url = u'https://graph.facebook.com/{0}/' \
#                       u'friends?fields=id,name,location,picture' \
#                       u'&amp;access_token={1}'.format(
#                           social_user.uid,
#                           social_user.extra_data['access_token'],
#                       )
#                 request = urllib2.Request(url)
#                 friends = json.loads(urllib2.urlopen(request).read()).get('data')
#                 for friend in friends:
#                     if (
#                         friend.get('location')
#                         and flight.arrival_airport.city
#                         and flight.arrival_airport.city.name
#                         in friend['location']['name']
#                     ):
#                         friends_in_city.append({
#                             'name': friend['name'],
#                             'photo': friend['picture']['data']['url'],
#                             'profile_url':
#                             'https://www.facebook.com/{0}'.format(friend['id']),
#                         })
#         context.update({
#             'friends_in_city': friends_in_city,
#         })
#         return context    
