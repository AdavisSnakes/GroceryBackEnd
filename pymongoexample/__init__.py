from flask import Flask
from .extensions import mongo
from .main import main

def create_app(config_object='pymongoexample.settings'):
    app = Flask(__name__)

    #load the settings file which has the MONGO_URI
    app.config.from_object(config_object)

    #Initialize this PyMongo for use
    mongo.init_app(app)

    app.register_blueprint(main)

    app.secret_key='secret123'

    return app
