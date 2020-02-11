from flask import Blueprint,jsonify, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from .extensions import mongo
from datetime import datetime
from pymongo import MongoClient
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug import secure_filename
import logging
import sys
from .parseRecipe import parseCSV, recipe

log = logging.getLogger(__name__)

main = Blueprint('main', __name__)
#consumer ID 28d3f573-6c8f-4ae3-905e-a7f0f4efcd76


#remote register


#***********
#api practice

@main.route('/api_test')
def api_test():
    items = []
    items.append({"cheese" : "1", "bread" : "white", "meat" : "steak"})
    items.append({"1" : "1", "2" : "2", "3" : "3"})
    return jsonify({'listTest' : items})

#/add_listItem
@main.route('/add_listItem', methods=['GET', 'POST'])
def add_listItem():
    data = request.get_json()
    print('****** Item: ' + data["listItem"])
    user_collection = mongo_user.db.users
    user_collection.insert({'Item' : data["listItem"]})
    return 'Done', 201

@main.route('/register', methods=['POST'])
def register():
    data=request.get_json()

    # place holders
    user = None
    first_name = None
    last_name = None
    password = None
    date = None
    success = False
    testprint = "testprint"

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

#if db.mycollection.find({'UserIDS': { "$in": newID}}).count() > 0.
#{
#	"user":"test",andrew
#	"name" : "Andrew"
#	"password": "1234",
#	"email" : "asdf@asdf.com"
#	"date" : "2020-3-3-10:22.100"
#}

#------
#Database practice

@main.route('/add')
def add():
    #user_collection = mongo_user.db.users
    #user_collection.insert({'name' : 'Emily', 'language' : 'Python'})
    #user_collection.insert({'name' : 'Frank', 'language' : 'C'})
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

#------
#Page practice

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Index
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
@is_logged_in
def dashboard():
        msg = 'Nothing Found'
        return render_template('dashboard.html', msg=msg)

# Load Recipes
class UploadForm(FlaskForm):
    file = FileField(validators=[
    FileRequired()#,
    #FileAllowed('.csv', 'csv\'s only!')
    ])

# WTforms User Register
@main.route('/loadRecipeList', methods=['GET', 'POST'])
def loadRecipeList():
    form = UploadForm()

    if form.validate_on_submit():
        print('*******************')
        #print('content: \n' + form.file.data.read().decode("utf-8"), file=sys.stdout)
        recipe = parseCSV.parse(form.file.data.read().decode("utf-8"))
        print('recipe.ingredients[0]=' + recipe.ingredients[0])
        print('*******************')
        flash('You loaded the files!', 'success')
        return redirect(url_for('main.loadRecipeList'))

    return render_template('loadRecipeList.html', form=form)


# WTforms Register Form Class - LOCAL
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# WTforms User Register - LOCAL
@main.route('/registerLOCAL', methods=['GET', 'POST'])
def registerLOCAL():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        register_date = datetime.today().strftime('%Y-%m-%d')

        flash('You are now registered and can login!', 'success')

        user_collection = mongo.db.users
        user_collection.insert({'name' : name, 'email' : email, 'username' : username, 'password' : password, 'register_date' : register_date})


        #return redirect(url_for('index'))
        return redirect(url_for('main.loginLOCAL'))
    return render_template('register.html', form=form)


# WTForms User login

# User login

@main.route('/loginLOCAL', methods=['GET', 'POST'])
def loginLOCAL():
    if request.method == 'POST':

        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Get user by username
        user_collection = mongo.db.users
        user = user_collection.find_one({'name' : 'Emily'})
        result = user_collection.count({'username' : username})

        if result > 0:
            # Get
            user = user_collection.find_one({'username' : username})
            password = user["password"]

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):

                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Logout
@main.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('main.login'))

if __name__ == '__main__':
    main.run(debug=True)
