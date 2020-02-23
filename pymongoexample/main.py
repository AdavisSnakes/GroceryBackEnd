from flask import Blueprint,jsonify, render_template, flash, redirect, url_for, session, logging, request
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime
from pymongo import MongoClient
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug import secure_filename
import logging
import sys

##
from .extensions import mongo
from .parseRecipe import parseCSV, recipe
from .registerFunctions import registerClass
from .localRegisterFunctions import localRegisterClass

#
log = logging.getLogger(__name__)
main = Blueprint('main', __name__)

#User session holder
userSessions = []

#******************************************************************8
#api
@main.route('/register', methods=['POST'])
def reg():
    return registerClass.register()

@main.route('/login', methods=['POST'])
def test():
    return registerClass.login()

@main.route('/loginRequiredRoute', methods=['POST'])
@login_required
def loginRequiredRoute():
    return 'loginRequiredRoute'

@main.route("/logout", methods=['POST'])
#@login_required
def logout():
    success = registerClass.logout
    if(success):
        return redirect('main.login')
    else:
        return {"pass" : False, "error" : "Missing Field"}

#*****************************************************************
#Database practice

@main.route('/add')
def add():
    user_collection = mongo.db.users
    user_collection.insert({'name' : "user3"})
    recipe_collection = mongo.db.users
    recipe_collection.insert({'name' : "recipe3"})
    return '<h1>Added a recipe!</h1>'

@main.route('/find')
def find():
    user_collection = mongo.db.users
    user = user_collection.find_one({'name' : 'Emily'})
    return f'<h1>User: { user["name"] } Language: { user["language"] }</h1>'

@main.route('/update')
def update():
    user_collection = mongo.db.users
    user = user_collection.find_one({'name' : 'Emily'})
    user["language"] = 'Ruby'
    user_collection.save(user)

    return '<h1>Updated user!</h1>'

@main.route('/delete')
def delete():
    user_collection = mongo.db.users
    user = user_collection.find_one({'name' : 'Brian'})
    user_collection.remove(user)

    return '<h1>Deleted User!</h1>'

#**************************************************************
# Load Recipes
class UploadForm(FlaskForm):
    file = FileField(validators=[
    FileRequired()])

# WTforms User Register
@main.route('/loadRecipeList', methods=['GET', 'POST'])
def loadRecipeList():
    form = UploadForm()

    if form.validate_on_submit():
        print('*******************')
        recipe = parseCSV.parse(form.file.data.read().decode("utf-8"))
        print('recipe.ingredients[0]=' + recipe.ingredients[0])
        print('*******************')
        flash('You loaded the files!', 'success')
        return redirect(url_for('main.loadRecipeList'))

    return render_template('loadRecipeList.html', form=form)


# LOCAL website
@main.route('/')
def index():
    return render_template('home.html')

@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

# Dashboard
@main.route('/dashboard')
def dashboard():
        msg = 'Nothing Found'
        return render_template('dashboard.html', msg=msg)

if __name__ == '__main__':
    main.run(debug=True)
