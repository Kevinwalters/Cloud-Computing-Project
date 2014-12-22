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
        
        publicEvents = events.find({"user_id" : ObjectId("111111111111111111111111")})
        
        if not publicEvents:
            return "fail"
        
        return dumps(publicEvents)
    
    @staticmethod
    def getFriendEvents(user_id):
        #user = UserController.getUser(user_id)
        #if not user or user == "fail":
        #    return "fail"

        #friends = UserController.getFacebookFriends(user['facebookId'])
        
        friends = UserController.getFacebookFriends(user_id)
        friendUsers = UserController.getUsersFromFriends(friends)
        
        client = MongoClient(System.URI)
        db = client.ConnectMe
        events = db.event
        
        friendEvents = events.find({"user_id" : {"$in" : friendUsers}})
        events_list = list()
        for event in friendEvents:
            events_list.append(event)
        
        return events_list
    
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
        if user_id not in event['attending_list']:
            event['attending_list'].append(user_id)
        events.save(event)
        print "User", user_id, "added to event", event_id
        result = CalendarController.addEvent(str(event_id), str(user_id))
        return result
                
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
        events.save(event)
        print "User", user_id, "left event", event_id
        CalendarController.removeEvent(str(event_id), str(user_id))
    
    #expect invite_list to be the IDs
    @staticmethod
    def createEvent(user_id, name, description, location, date, start_time, end_time, tags, is_private, invite_list):
        print "Before casting"
        try:
            user_id = ObjectId(user_id)
            for invitee in invite_list:
                invitee = ObjectId(invitee)
        except:
            print "A user could not be cast to an ObjectId"
            return "fail"
        print "All successfully casted"
        attending_list = list()
        attending_list.append(user_id)
        event = Event(user_id=user_id, name=name, description=description, location=location, date=date, start_time=start_time, end_time=end_time, tags=tags, is_private=is_private, invite_list=invite_list, attending_list=attending_list)
        new_event = event.save()
        event_id = new_event.id
        print "Event", new_event.id, "created by user", user_id
        for invitee in invite_list:
            EventController.sendInvite(event_id, invitee)
        result = CalendarController.addEvent(str(event_id), str(user_id))
        return result
        #TODO call SNS, push to all maps - show on map if: friends with user_id, or is_private is false
    
    @staticmethod
    def sendInvite(event_id, user_id):
        result = CalendarController.addEvent(event_id, user_id, True)
        return result
        
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
        print "Deleted event", event_id
    
    @staticmethod
    def deleteEvents():
        client = MongoClient(System.URI)
        db = client.ConnectMe
        events = db.event
        
        events.remove({})
