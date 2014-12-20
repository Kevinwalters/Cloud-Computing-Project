from bson.json_util import dumps
from bson.objectid import ObjectId
from django.http import HttpResponse
from pymongo.mongo_client import MongoClient

from ConnectMeApp import System
from models import User


System=System

class UserController:
    
    #@staticmethod
    #def createUser(...):
    #TODO...what kind of FB data do we get?
    @staticmethod
    def login(email, password):
        print "email:", email, "password:", password
        return "test_userid"
    
    @staticmethod
    def getAllUsers(request):
        client = MongoClient(System.URI)
        db = client.app
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
        db = client.app
        users = db.user
        user = users.find_one({"_id": user_id})
        
        return user
    
    