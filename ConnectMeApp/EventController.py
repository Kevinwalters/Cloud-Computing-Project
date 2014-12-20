from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient

from CalendarController import CalendarController
from System import System
from UserController import UserController
from models import Event
from bson.json_util import dumps

class EventController:
    def __init__(self):
        pass
    
    @staticmethod
    def getPublicEvents():
        client = MongoClient(System.URI)
        db = client.ConnectMe
        events = db.event
        
        publicEvents = events.find({"user_id" : "Public API"})
        
        if not publicEvents:
            return "fail"
        
        return dumps(publicEvents)
    
    @staticmethod
    def getFriendEvents(user_id):
        user = UserController.getUser(user_id)
        friends = UserController.getFacebookFriends(user['facebook_id'])
        
        friend_ids = list()
        for friend in friends:
            friend_ids.append(friend['_id'])
        
        client = MongoClient(System.URI)
        db = client.ConnectMe
        events = db.event
        
        friendEvents = events.find({"user_id" : {"$in" : friend_ids}})
        
        return dumps(friendEvents)
    
    @staticmethod
    def joinEvent(user_id, event_id):
        try:
            user_id = ObjectId(user_id)
            event_id = ObjectId(event_id)
        except:
            return "fail"
        
        client = MongoClient(System.URI)
        db = client.ConnectMe
        events = db.event
        
        event = events.find_one({"_id" : event_id})
        if not event:
            return "fail"
        
        if user_id in event['invite_list']:
            event['invite_list'].remove(user_id)
        event['attending_list'].append(user_id)
        CalendarController.addEvent(str(event_id), str(user_id))
                
    @staticmethod
    def leaveEvent(user_id, event_id):
        try:
            user_id = ObjectId(user_id)
            event_id = ObjectId(event_id)
        except:
            return "fail"
        
        client = MongoClient(System.URI)
        db = client.ConnectMe
        events = db.event
        
        event = events.find_one({"_id" : event_id})
        
        if user_id in event['attending_list']:
            event['attending_list'].remove(user_id)
        CalendarController.removeEvent(str(event_id), str(user_id))
    
    #expect invite_list to be the IDs
    @staticmethod
    def createEvent(user_id, name, description, location, date, start_time, end_time, tags, is_private, invite_list):
        try:
            user_id = ObjectId(user_id)
            for invitee in invite_list:
                invitee = ObjectId(invitee)
        except:
            return "fail"
        event = Event(user_id, name, description, location, date, start_time, end_time, tags, is_private, invite_list)
        new_event = event.save()
        event_id = new_event['_id']
        for invitee in invite_list:
            EventController.sendInvite(event_id, invitee)
            
        result = CalendarController.addEvent(str(event_id), str(user_id))
        if result == "fail":
            return result
        #TODO call SNS, push to all maps - show on map if: friends with user_id, or is_private is false
    
    @staticmethod
    def sendInvite(event_id, user_id):
        CalendarController.addEvent(event_id, user_id, True)
        
    #remove event from invitees, people who have joined, and the creator's calendars
    @staticmethod
    def deleteEvent(event_id):
        try:
            event_id = ObjectId(event_id)
        except:
            return "fail"
        client = MongoClient(System.URI)
        db = client.ConnectMe
        events = db.event
        
        event = events.find_one({"_id": event_id})
        for user in event['invite_list']:
            CalendarController.removeEvent(str(event_id), str(user))
        for user in event['attending_list']:
            CalendarController.removeEvent(str(event_id), str(user))
        CalendarController.removeEvent(str(event_id), str(event['user_id']))
        events.remove({"_id": event_id})
        
    @staticmethod
    def getEventDetails(event_ids): #takes a list of event IDs (already ObjectIds)
        client = MongoClient(System.URI)
        db = client.ConnectMe
        events = db.event
     
        attendingEvents = events.find({"_id" : {"$in" : event_ids}})
        
        return attendingEvents