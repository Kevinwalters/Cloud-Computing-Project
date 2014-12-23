import ast
import json
import urllib2

from bson.json_util import dumps
from bson.objectid import ObjectId
from django.http import HttpResponse
from pymongo.mongo_client import MongoClient

from System import System
from models import User
from CalendarController import CalendarController

class UserController:
    
    @staticmethod
    def createUser(name, facebookId, accessToken, pictureURL):
        user = User(name, facebookId, accessToken, pictureURL)
        user = user.save()
        
        print "created user:", user.id 
        
        CalendarController.createCalendar(user.id)
        
        return user.id
    
    @staticmethod
    def login(name, facebookId, accessToken, pictureURL):
        client = MongoClient(System.URI)
        db = client.ConnectMe
        users = db.user
        
        user = users.find_one({"facebookId" : facebookId})
        
        if user:
            result = user['_id']
        else:
            user = UserController.createUser(name, facebookId, accessToken, pictureURL)
            result = user
        if not user:
            return "fail"
        return result
        
    
    @staticmethod
    def getAllUsers(request):
        client = MongoClient(System.URI)
        db = client.ConnectMe
        users = db.user
        user_list = list()
        for user_data in users.find():
            user_list.append(user_data.getJson())
        return HttpResponse(user_list)     
    
    @staticmethod
    def getUser(user_id):
        try:
            user_id = ObjectId(user_id)
        except:
            return "fail"
        client = MongoClient(System.URI)
        db = client.ConnectMe
        users = db.user
        
        user = users.find_one({"_id": user_id})
        
        return user
    
    @staticmethod
    def getUsersFromFriends(friends):
        client = MongoClient(System.URI)
        db = client.ConnectMe
        users = db.user
        
        friendList = users.find({"facebookId": {"$in" : friends}})
        
        friends = list()
        for friend in friendList:
            friends.append(friend['_id'])
        
        return friends
    
    @staticmethod
    def getFacebookFriends(user_id):
        try:
            user_id = ObjectId(user_id)
        except:
            return "fail"
        
        client = MongoClient(System.URI)
        db = client.ConnectMe
        #fbUsers = db.social_auth_usersocialauth
        users = db.user
        
        user = users.find_one({"_id": user_id})
        
        print user
        if not user:
            return "fail"
        
        accessToken = user['access_token']
        print accessToken
        print user['facebookId']

        url = u'https://graph.facebook.com/{0}/' \
            u'friends?fields=id,name,location,picture' \
            u'&access_token={1}'.format(user['facebookId'], accessToken)
        request = urllib2.Request(url)
        friends = json.loads(urllib2.urlopen(request).read()).get('data')

        friend_ids = list()
        for friend in friends:
            friend_ids.append(friend['id'])
            
        return friend_ids
    
    @staticmethod
    def getMultiUser(user_ids):
        user_ids = user_ids.split(',')
        user_obj_ids = list()
        try:
            for user_id in user_ids:
                user_obj_ids.append(ObjectId(user_id))
        except:
            return "fail"
        
        client = MongoClient(System.URI)
        db = client.ConnectMe
        users = db.user
        print user_obj_ids
        
        userList = users.find({"_id": {"$in" : user_obj_ids}})
        
        if not userList:
            return "fail"
        
        return dumps(userList)
