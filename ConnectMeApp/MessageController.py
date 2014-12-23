import datetime
from models import Message
from bson.objectid import ObjectId

#this controller was never implemented as we hit a roadblock, and due to time constraints were unable to do messaging
class MessageController:
    
    #create a message for the event
    @staticmethod
    def createMessage(sender_id, event_id, message, time):
        try:
            sender_id = ObjectId(sender_id)
            event_id = ObjectId(event_id)
        except:
            return "fail"
        message = Message(sender_id, event_id, message, time)
        message_id = message.save()
        if not message_id:
            return "fail"
        
    #send a message for the event
    @staticmethod
    def sendMessage(sender_id, event_id, message):
        time = datetime.datetime.now()
        result = MessageController.createMessage(sender_id, event_id, message, time)
        if result == "fail":
            return "fail"
        MessageController.sendSNS(sender_id, event_id, message, time)#use SNS to send to all monitoring that event
        
    @staticmethod
    def sendSNS(sender_id, event_id, message, time):
        pass#TODO