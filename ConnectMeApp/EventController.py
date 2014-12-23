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
    
    #gets all events - both public and of your friends
    @staticmethod
    def getPublicEvents():
        client = MongoClient(System.URI)
        db = client.ConnectMe
        events = db.event
        
        publicEvents = events.find()#{"user_id" : ObjectId("111111111111111111111111")})
        
        if not publicEvents:
            return "fail"
        
        return dumps(publicEvents)
    
    #gets all events created by one of your friends
    @staticmethod
    def getFriendEvents(user_id):
        friends = UserController.getFacebookFriends(user_id) #get your facebook friends (facebookIds)
        friendUsers = UserController.getUsersFromFriends(friends) #turn these facebookIds into user_ids
        
        client = MongoClient(System.URI)
        db = client.ConnectMe
        events = db.event
        
        if not friendUsers or len(friendUsers) == 0: #return empty list, for formatting purposes
            return list()
        
        friendEvents = events.find({"user_id" : {"$in" : friendUsers}}) #get all events where the user_id of who created it is in the list of your friends' IDs
        events_list = list()
        for event in friendEvents:
            events_list.append(event)
        
        return events_list
    
    #have the given user attend the event
    @staticmethod
    def joinEvent(user_id, event_id):
        try:
            user_id = ObjectId(user_id)
            event_id = ObjectId(event_id)
        except:
            print "Invalid object id"
            return "fail"
        
        print event_id
        
        client = MongoClient(System.URI)
        db = client.ConnectMe
        events = db.event
        
        event = events.find_one({"_id" : event_id}) #get the full event object
        if not event:
            print "event not found"
            return "fail"
        
        if user_id in event['invite_list']: #remove from the invite list if the user was invited
            event['invite_list'].remove(user_id)
        if user_id not in event['attending_list']: #add the user to the attending list
            event['attending_list'].append(user_id)
        events.save(event)
        print "User", user_id, "added to event", event_id
        result = CalendarController.addEvent(str(event_id), str(user_id)) #add the event to the user's calendar
        return result
                
    #have the user leave the event
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
        
        event = events.find_one({"_id" : event_id}) #get the full event object
        
        if user_id in event['attending_list']:
            event['attending_list'].remove(user_id) #remove the user from the event's attending list
        events.save(event)
        print "User", user_id, "left event", event_id
        CalendarController.removeEvent(str(event_id), str(user_id)) #remove the event from the user's calendar
    
    #create a new event
    @staticmethod
    def createEvent(user_id, name, description, latitude, longitude, date, start_time, end_time, tags, is_private, invite_list): #invite_list is currently facebook IDs
        print "Before casting"
        try:
            user_id = ObjectId(user_id)
            if invite_list[0] == "" or invite_list == "\"\"":
                invite_list = list()
        except:
            print "A user could not be cast to an ObjectId"
            return "fail"
        print "All successfully casted"
        
        client = MongoClient(System.URI)
        db = client.ConnectMe
        users = db.user
        
        our_users = users.find({"facebookId":  {"$in" : invite_list}}) #gets users to invite, based on the provided facebook IDs
        
        ids = list()
        for user in our_users:
            ids.append(user['_id'])
        
        attending_list = list()
        attending_list.append(user_id)#add the event creator to the attending list
        event = Event(user_id=user_id, name=name, description=description, latitude=latitude, longitude=longitude, date=date, start_time=start_time, end_time=end_time, tags=tags, is_private=is_private, invite_list=ids, attending_list=attending_list)
        new_event = event.save()#create the event
        event_id = new_event.id
        print "Event", new_event.id, "created by user", user_id
        for invitee in ids:
            EventController.sendInvite(event_id, invitee) #invite each of the users to the event
        result = CalendarController.addEvent(str(event_id), str(user_id))#add this event to the creator's calendar
        return result
    
    #send an invite to an event to a user
    @staticmethod
    def sendInvite(event_id, user_id):
        result = CalendarController.addEvent(event_id, user_id, True)#add an "invite" event to the friend's calendar
        return result
        
    #delete the event - remove event from invitees, people who have joined, and the creator's calendars
    @staticmethod
    def deleteEvent(event_id):
        try:
            event_id = ObjectId(event_id)
        except:
            return "fail"
        client = MongoClient(System.URI)
        db = client.ConnectMe
        events = db.event
        
        event = events.find_one({"_id": event_id}) #get the full event
        for user in event['invite_list']:
            CalendarController.removeEvent(str(event_id), str(user)) #remove event from each user's calendar
        for user in event['attending_list']:
            CalendarController.removeEvent(str(event_id), str(user)) #remove event from each user's calendar
        CalendarController.removeEvent(str(event_id), str(event['user_id'])) #remove event from the creator's calendar
        events.remove({"_id": event_id}) #remove from the database
        print "Deleted event", event_id
    
    #delete all events from the database - not used b
    @staticmethod
    def deleteEvents():
        client = MongoClient(System.URI)
        db = client.ConnectMe
        events = db.event
        
        events.remove({})
        
    #get full details about an event
    @staticmethod
    def getEvent(event_id):
        try:
            event_id = ObjectId(event_id)
        except:
            return "fail"
        client = MongoClient(System.URI)
        db = client.ConnectMe
        events = db.event
     
        event = events.find_one({"_id" : event_id})#get the event given its id
        if not event:
            return "fail"
        return event
