from flask import Blueprint, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from .extensions import mongo
from datetime import datetime

main = Blueprint('main', __name__)


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

#------
#Page practice

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

@main.route('/login')
def login():
    return render_template('login.html')


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



if __name__ == '__main__':
    main.run(debug=True)


#ID
#name
#email
#username
#password
#register_date
#
