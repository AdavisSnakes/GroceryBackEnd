from flask import Flask
from .extensions import mongo, login_manager
from .main import main


def create_app(config_object='pymongoexample.settings'):
    app = Flask(__name__)

    #load the settings file which has the MONGO_URI
    app.config.from_object(config_object)

    #Initialize this PyMongo for use
    mongo.init_app(app)

    # blueprint for non-authorized routes
    app.register_blueprint(main)

    # login Login Manager
    login_manager.init_app(app)

    # TODO hide the secret key
    app.secret_key='secret123'

    return app
