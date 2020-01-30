from flask import Blueprint,jsonify, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from .extensions import mongo
from datetime import datetime
import logging
import sys

log = logging.getLogger(__name__)

main = Blueprint('main', __name__)


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
    user_collection = mongo.db.users
    user_collection.insert({'Item' : data["listItem"]})
    return 'Done', 201

@main.route('/returnItems')
def returnItems():
    returnList = []
    user_collection = mongo.db.users
    item = user_collection.find({'Item': {'$exists': True} })
    for doc in item:
        #print(doc["Item"])
        returnList.append({'item' : str(doc["Item"])})
    #return '<h1>test</h1>'
    return jsonify({'itemlist' : returnList})

#------
#Database practice

@main.route('/add')
def add():
    user_collection = mongo.db.users
    user_collection.insert({'name' : 'Emily', 'language' : 'Python'})
    user_collection.insert({'name' : 'Frank', 'language' : 'C'})
    return '<h1>Added a User!</h1>'

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

@main.route('/test')
def test():
        user_collection = mongo.db.users
        user = user_collection.find_one({'name' : 'Emily'})
        user1 = user["language"]
        return f'<h1>user: {user1}</h1>'

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

@main.route('/debug')
def debug():
    log.debug('This is debug***********************')
    log.info('This is info*')
    log.warn('This is warn**')
    log.fatal('This is fatal***')
    print('This is error output', file=sys.stderr)
    print('This is standard output', file=sys.stdout)
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

# WTforms Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# WTforms User Register
@main.route('/register', methods=['GET', 'POST'])
def register():
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
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


# WTForms User login

# User login

@main.route('/login', methods=['GET', 'POST'])
def login():
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


#ID
#name
#email
#username
#password
#register_date
#
