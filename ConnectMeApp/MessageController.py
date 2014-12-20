import datetime
from models import Message
from bson.objectid import ObjectId

class MessageController:
    
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
        
    @staticmethod
    def sendMessage(sender_id, event_id, message):
        time = datetime.datetime.now()
        result = MessageController.createMessage(sender_id, event_id, message, time)
        if result == "fail":
            return "fail"
        MessageController.sendSNS(sender_id, event_id, message, time)
        
    @staticmethod
    def sendSNS(sender_id, event_id, message, time):
        #TODO