from flask import Blueprint,jsonify, render_template, flash, redirect, url_for, session, logging, request
from .extensions import mongo


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

class localRegisterClass:
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

#if db.mycollection.find({'UserIDS': { "$in": newID}}).count() > 0.
#{
#	"user":"test",andrew
#	"name" : "Andrew"
#	"password": "1234",
#	"email" : "asdf@asdf.com"
#	"date" : "2020-3-3-10:22.100"
#}
