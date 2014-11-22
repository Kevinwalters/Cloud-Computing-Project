from mongoengine import *
import datetime

connect('db')

class User(Document):    
    #user_id = ObjectIdField(default=None)
    name = StringField()
    email = EmailField()
    password = StringField()
    salt = StringField()
    email_alerts = BooleanField(default=True)
    alert_frequency = StringField(default='Weekly')
    friends = ListField(ReferenceField('self'))
    friend_requests = ListField(ReferenceField('self'))
    pending_friend_requests = ListField(ReferenceField('self'))
    validate_url = StringField()
    is_validated = BooleanField(default=False)
    validate_set_date = LongField()

class Calendar(Document):
    user_id = ReferenceField('User')
    events = ListField(ReferenceField('Event'))

class Event(Document):
    loc = StringField()
    date = DateTimeField()
    name = StringField()
    description = StringField()
    url = URLField()
    category = StringField()

class Subscription(Document):
    user_id = ReferenceField('User')
    query = StringField()
