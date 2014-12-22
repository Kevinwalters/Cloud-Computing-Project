from django.db import models

# Create your models here.
from mongoengine import *
import datetime

connect('ConnectMe', host="mongodb://cccc:12345678@ec2-54-173-96-92.compute-1.amazonaws.com:27017/ConnectMe")


class User(Document):    #TODO may need to store FB ID separately, not as _id - may not be valid mongo id
    name = StringField()
    facebookId = StringField()
    access_token = StringField()
    pictureURL = StringField()

class Calendar(Document):
    user_id = ReferenceField('User')
    events = ListField(ReferenceField('Event'), default=list())
    invited_events = ListField(ReferenceField('Event'), default=list())

class Event(Document):
    user_id = ReferenceField('User') #creator
    name = StringField()
    description = StringField()
    latitude = StringField()
    longitude = StringField()
    date = StringField()
    start_time = StringField()
    end_time = StringField
    tags = ListField(StringField())
    is_private = BooleanField()
    invite_list = ListField(ReferenceField('User'))
    attending_list = ListField(ReferenceField('User'))

class Message(Document):
    sender_id = ReferenceField('User')
    event_id = ReferenceField('Event')
    message = StringField()
    time = DateTimeField()
