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


main = Blueprint('main', __name__)

@main.route('/test')
def test:
    return 'hi'
