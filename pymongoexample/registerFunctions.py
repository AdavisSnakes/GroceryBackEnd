from flask import Blueprint,jsonify, render_template, flash, redirect, url_for, session, logging, request
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from .extensions import mongo, login_manager
from .userClass import User

class registerClass:
    #**********************
    # log in the user
    def login():
        #get the json data
        data=request.get_json()
        #create user object
        user = User()

        #did we find the needed info in data?
        if 'user' and 'password' in data:
            #get the database and  load data into user
            user_collection = mongo.db.users
            user.getUserData(data)

            if(user_collection.find({'username' : user.username, 'password' : user.password}).count() == 1):
                theUser = user_collection.find_one({'username' : user.username, 'password' : user.password})
                #set user id for the user class. The login class need the id attributes to be set
                user.id = theUser["_id"]
                login_user(user)
                return {"pass" : True}
            elif(user_collection.find({'username' : username, 'password' : password}).count() > 0):
                return {"pass" : False, "error" : "more than 1 user found"}
            elif((user_collection.find({'username' : username, 'password' : password}).count() == 0)):
                return {"pass" : False, "error" : "User not found"}
            else:
                return {"pass" : False, "error" : "User error"} # shouldn't get here
        else:
            return {"pass" : False, "error" : "user and password combo not found"}



#**********************
    # register the user
    def register():
        data=request.get_json()
        success = False
        user = User()

        #if all the needed fields are found
        if 'user' and 'first name' and 'last name' and 'password' and 'email' and 'date' in data:
            user.getUserData(data)
            success = True

        # if all the fields were found
        if success == True:
            user_collection = mongo.db.users
            # if the user exists
            if(user_collection.find({'username' : user.username}).count()>0):
                return {"pass" : False,"error" : "Username Exists"}
            else:
                user_collection.insert({
                'username' : user.username,
                'first_name' : user.firstName,
                'last_name' : user.lastName,
                'password' : user.password,
                'date' : user.date
                })
                return {"pass" : True}

        return {"pass" : False, "error" : "Missing Field"}

#**********************
    # somewhere to logout
    def logout():
        logout_user()
        return 'True'


    # handle login failed
    def page_not_found(e):
        return '<p>Login failed</p>'


    @login_manager.user_loader
    def load_user(user_id):
        return User.id
