from bson.json_util import dumps
from django.http import HttpResponse
from pymongo.mongo_client import MongoClient

from System import System
from models import User


class UserController:
    
    #@staticmethod
    #def createUser(...):
    #TODO...what kind of FB data do we get?
    
    
    @staticmethod
    def getAllUsers(request):
        client = MongoClient(System.URI)
        db = client.obo
        users = db.user
        user_list = list()
        for user_data in users.find():
            user_list.append(user_data.getJson())
        return HttpResponse(user_list)        

    @staticmethod
    def getUser(user_id):
        client = MongoClient(System.URI)
        db = client.obo
        users = db.user
        user = users.find_one({"_id": user_id})
        return dumps(user)
    
    