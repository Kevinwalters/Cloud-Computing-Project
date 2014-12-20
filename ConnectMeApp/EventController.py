from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from ConnectMeApp import CalendarController
from ConnectMeApp import System
from models import Event


System=System
CalendarController=CalendarController


class EventController:
    def __init__(self):
        pass
    
    
    @staticmethod
    def joinEvent(user_id, event_id):
        try:
            user_id = ObjectId(user_id)
            event_id = ObjectId(event_id)
        except:
            return "fail"
        
        client = MongoClient(System.URI)
        db = client.app
        events = db.event
        
        event = events.find_one({"_id" : event_id})
        
        if user_id in event['invite_list']:
            if user_id not in event['attending_list']:
                event['attending_list'].append(user_id)
            CalendarController.addEvent(event_id, user_id)
            event['invite_list'].remove(user_id)
        else:
            if user_id not in event['attending_list']:
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
        db = client.app
        events = db.event
        
        event = events.find_one({"_id" : event_id})
        
        if user_id in event['attending_list']:
            event['attending_list'].remove(user_id)
        CalendarController.removeEvent(str(event_id), str(user_id))
    
    #expect invite_list to be the IDs
    @staticmethod
    def createEvent(user_id, name, description, location, start_time, end_time, tags, is_private, invite_list):
        try:
            user_id = ObjectId(user_id)
            for invitee in invite_list:
                invitee = ObjectId(invitee)
        except:
            return "fail"
        event = Event(user_id, name, description, location, start_time, end_time, tags, is_private, invite_list)
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
        db = client.app
        events = db.event
        
        event = events.find_one({"_id": event_id})
        for user in event['invite_list']:
            CalendarController.removeEvent(str(event_id), str(user))
        for user in event['attending_list']:
            CalendarController.removeEvent(str(event_id), str(user))
        CalendarController.removeEvent(str(event_id), str(event['creator']))
        events.remove({"_id": event_id})