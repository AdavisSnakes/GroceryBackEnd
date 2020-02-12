from flask import Blueprint,jsonify, render_template, flash, redirect, url_for, session, logging, request
from .extensions import mongo

class registerClass:
    # log in the user
    def login():

        data=request.get_json()
        user = None
        password = None
        success = False

        if 'user' and 'password' in data:
            user_collection = mongo.db.users
            username = data['user']
            password = data['password']
            success = True

            if(user_collection.find({'username' : username, 'password' : password}).count() == 1):
                return {"pass" : True}
            elif(user_collection.find({'username' : username, 'password' : password}).count() > 0):
                return {"pass" : False, "error" : "more than 1 user found"}
            elif((user_collection.find({'username' : username, 'password' : password}).count() == 0)):
                return {"pass" : False, "error" : "User not found"}

    # register the user
    def register():
        data=request.get_json()

        # place holders
        user = None
        first_name = None
        last_name = None
        password = None
        date = None
        success = False

        #if all the needed fields are found
        if 'user' and 'first name' and 'last name' and 'password' and 'email' and 'date' in data:
            username = data['user']
            first_name = data['first name']
            last_name = data['last name']
            password = data['password']
            date = data['date']
            success = True

        # if all the fields were found
        if success == True:
            user_collection = mongo.db.users
            # if the user exists
            if(user_collection.find({'username' : username}).count()>0):
                return {"pass" : False,"error" : "Username Exists"}
            else:
                user_collection.insert({
                'username' : username,
                'first_name' : first_name,
                'last_name' : last_name,
                'password' : password,
                'date' : date
                })
                return {"pass" : True}

        return {"pass" : False, "error" : "Missing Field"}
