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
    
    #creates a new user - called if this is the first time authenticating a user
    @staticmethod
    def createUser(name, facebookId, accessToken, pictureURL):
        user = User(name, facebookId, accessToken, pictureURL)
        user = user.save()
        
        print "created user:", user.id 
        
        CalendarController.createCalendar(user.id) #creates a calendar for this user
        
        return user.id
    
    #login this user; since Facebook handles all authentication, we just need to return a user_id
    #we also create the user if it is their first time authenticating
    @staticmethod
    def login(name, facebookId, accessToken, pictureURL):
        client = MongoClient(System.URI)
        db = client.ConnectMe
        users = db.user
        
        user = users.find_one({"facebookId" : facebookId}) #checks if this facebook id is already in our database
        
        if user:
            result = user['_id']
        else:
            user = UserController.createUser(name, facebookId, accessToken, pictureURL) #create a new user if not in our database
            result = user
        if not user:
            return "fail"
        return result
        
    #returns a list of all users
    @staticmethod
    def getAllUsers(request):
        client = MongoClient(System.URI)
        db = client.ConnectMe
        users = db.user
        user_list = list()
        for user_data in users.find():
            user_list.append(user_data.getJson())
        return HttpResponse(user_list)     
    
    #returns the full user for this user id
    @staticmethod
    def getUser(user_id):
        try:
            user_id = ObjectId(user_id)
        except:
            return "fail"
        client = MongoClient(System.URI)
        db = client.ConnectMe
        users = db.user
        
        user = users.find_one({"_id": user_id}) #get the user that matches this id
        
        return user
    
    #given a list of facebookIds, returns their associated user_ids in our own database
    @staticmethod
    def getUsersFromFriends(friends):
        client = MongoClient(System.URI)
        db = client.ConnectMe
        users = db.user
        
        friendList = users.find({"facebookId": {"$in" : friends}}) #finds all users with facebookId field in the list of facebookIds provided
        
        friends = list()
        for friend in friendList:
            friends.append(friend['_id']) #generate a list of user_ids
        
        return friends
    
    #gets the facebook friends of the provided user
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
        
        user = users.find_one({"_id": user_id}) #get the user object associated with this id
        
        print user
        if not user:
            return "fail"
        
        #get the user's access token and facebook ID, which were stored in our database
        accessToken = user['access_token']
        print accessToken
        print user['facebookId']

        #get the user's friends
        url = u'https://graph.facebook.com/{0}/' \
            u'friends?fields=id,name,location,picture' \
            u'&access_token={1}'.format(user['facebookId'], accessToken)
        request = urllib2.Request(url)
        friends = json.loads(urllib2.urlopen(request).read()).get('data')

        friend_ids = list()
        for friend in friends:
            friend_ids.append(friend['id']) #we only need the friend IDs
            
        return friend_ids
    
    #given multiple user ids, return the list of their full user objects
    @staticmethod
    def getMultiUser(user_ids):
        user_ids = user_ids.split(',')#ids come in a a comma-separated list
        user_obj_ids = list()
        try:
            for user_id in user_ids:
                user_obj_ids.append(ObjectId(user_id)) #cast each id as an ObjectId
        except:
            return "fail"
        
        client = MongoClient(System.URI)
        db = client.ConnectMe
        users = db.user
        print user_obj_ids
        
        userList = users.find({"_id": {"$in" : user_obj_ids}}) #find all users with a user_id in the list provided
        
        if not userList:
            return "fail"
        
        return dumps(userList)
