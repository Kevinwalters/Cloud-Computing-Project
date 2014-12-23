from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from System import System
from models import Calendar

class CalendarController:
    def __init__(self):
        pass
    
    #creates a calendar for the provided user
    @staticmethod
    def createCalendar(user_id):
        try:
            user_id = ObjectId(user_id)
        except:
            return "fail"
        calendar = Calendar(user_id)#create the calendar
        cal = calendar.save()
        print "created calendar:", cal.id
        return dumps(cal)#return the calendar object
    
    #deletes the calendar for the provided user
    @staticmethod
    def delete(user_id):
        try:
            user_id = ObjectId(user_id)
        except:
            return "fail"
        client = MongoClient(System.URI)
        db = client.ConnectMe
        calendars = db.calendar
        calendars.remove({"user_id": user_id})
    
    #returns the entire calendar for the user
    @staticmethod
    def getCalendar(user_id):
        try:
            user_id = ObjectId(user_id)
        except:
            return "fail"
        client = MongoClient(System.URI)
        db = client.ConnectMe
        calendars = db.calendar
        calendar = calendars.find_one({"user_id": user_id})#gets the calendar for this user
        #print calendar
        if not calendar:
            return None
        return dumps(calendar)
    
    #add the given event to this user's calendar
    @staticmethod
    def addEvent(event_id, user_id, is_invite=False):
        try:
            event_id = ObjectId(event_id)
            user_id = ObjectId(user_id)
        except:
            print "failed converting to ObjectIds"
            return "fail"
        client = MongoClient(System.URI)
        db = client.ConnectMe
        calendars = db.calendar
        
        calendar = calendars.find_one({"user_id": user_id}) #get this user's calendar
        if not calendar:
            print "Calendar not found for user:", user_id
            return "fail"
        if is_invite and event_id not in calendar['invited_events']: #if the user is being invited, add the event to their invited events list
            calendar['invited_events'].append(event_id)
        elif not is_invite and event_id not in calendar['events']: #user is not being invited, so they are attending - add to their events list
            calendar['events'].append(event_id)
            if event_id in calendar['invited_events']:
                calendar['invited_events'].remove(event_id) #remove from their invited list if they were invited before joining
        calendars.save(calendar)
        print "Event", event_id, "added to Calendar", calendar['_id'], "for user", user_id
        return "success"
        
    #remove an event from this user's calendar
    @staticmethod
    def removeEvent(event_id, user_id):
        try:
            if not user_id == "Public API":
                user_id = ObjectId(user_id)
            event_id = ObjectId(event_id)
        except:
            return "fail"
        client = MongoClient(System.URI)
        db = client.ConnectMe
        calendars = db.calendar
        calendar = calendars.find_one({"user_id": user_id}) #get this user's calendar
        if not calendar:
            return "fail"
        if event_id in calendar['events']: #remove from his events list if it's in there
            calendar['events'].remove(event_id)
        if event_id in calendar['invited_events']: #remove from his invited list if it's in there
            calendar['invited_events'].remove(event_id)
        print "Event", event_id, "removed from calendar", calendar['_id'], "for user", user_id
        calendars.save(calendar)
        return "success"
    
    #get a list of all events this user is attending
    @staticmethod
    def getAttendingEvents(user_id):
        try:
            user_id = ObjectId(user_id)
        except:
            return "fail"
        
        client = MongoClient(System.URI)
        db = client.ConnectMe
        calendars = db.calendar
        calendar = calendars.find_one({"user_id": user_id}) #get this user's calendar
        
        if not calendar:
            return "fail"
        
        attendingEvents = CalendarController.getEventDetails(calendar['events'])#get the details for the event ids
        
        return dumps(attendingEvents)
    
    #gets a list of all events this user was invited to
    @staticmethod
    def getInvitedEvents(user_id):
        try:
            user_id = ObjectId(user_id)
        except:
            return "fail"
        
        client = MongoClient(System.URI)
        db = client.ConnectMe
        calendars = db.calendar
        calendar = calendars.find_one({"user_id": user_id}) #get this user's calendar
        
        if not calendar:
            return "fail"
        
        invitedEvents = CalendarController.getEventDetails(calendar['invited_events']) #get the details for these invited event ids
        
        return dumps(invitedEvents)
    
    
    #returns the whole objects, rather than just the ids
    @staticmethod
    def getEventDetails(event_ids): #takes a list of event IDs (already ObjectIds)
        client = MongoClient(System.URI)
        db = client.ConnectMe
        events = db.event
     
        attendingEvents = events.find({"_id" : {"$in" : event_ids}}) #find all event objects that have an id in the list provided
        
        return attendingEvents
