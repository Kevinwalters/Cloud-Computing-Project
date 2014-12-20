from django.db import models

# Create your models here.
from mongoengine import *
import datetime

connect('ConnectMe')

class User(Document):    #TODO may need to store FB ID separately, not as _id - may not be valid mongo id
    name = StringField()
    email = EmailField()

class Calendar(Document):
    user_id = ReferenceField('User')
    events = ListField(ReferenceField('Event'))
    invited_events = ListField(ReferenceField('Event'))

class Event(Document):
    creator = ReferenceField('User')
    name = StringField()
    description = StringField()
    location = StringField()
    start_time = DateTimeField()
    end_time = DateTimeField
    tags = ListField(StringField())
    is_private = BooleanField(default=False)
    invite_list = ListField(ReferenceField('User'))
    attending_list = ListField(ReferenceField('User'))

class Message(Document):
    sender_id = ReferenceField('User')
    event_id = ReferenceField('Event')
    message = StringField()
    time = DateTimeField()