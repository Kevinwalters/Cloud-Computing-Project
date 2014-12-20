from django.db import models

# Create your models here.
from mongoengine import *
import datetime

connect('ConnectMe', host="mongodb://cccc:12345678@ec2-54-173-96-92.compute-1.amazonaws.com:27017/ConnectMe")


class User(Document):    #TODO may need to store FB ID separately, not as _id - may not be valid mongo id
    name = StringField()
    facebookId = StringField()

class Calendar(Document):
    user_id = StringField()
    events = ListField(ReferenceField('Event'))
    invited_events = ListField(ReferenceField('Event'))

class Event(Document):
    user_id = StringField()#ReferenceField('User') #creator
    name = StringField()
    description = StringField()
    location = StringField()
    date = DateTimeField()
    start_time = DateTimeField()
    end_time = DateTimeField
    tags = ListField(StringField())
    is_private = BooleanField(default=False)
    invite_list = ListField(ReferenceField('User'), default=list())
    attending_list = ListField(ReferenceField('User'), default=list())

class Message(Document):
    sender_id = ReferenceField('User')
    event_id = ReferenceField('Event')
    message = StringField()
    time = DateTimeField()
