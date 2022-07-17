__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import os
import sys
import dash
import sqlite3
import logging, logging.config
import dash_bootstrap_components as dbc
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config.applogger import app_loggers
from sqlalchemy import Table, create_engine
from callbacks.callbacks_authentication import callback_manager as authentication_callback_manager
from callbacks.callbacks_sidepanel import callback_manager as sidepanel_callback_manager
from callbacks.callbacks_retail_summary import callback_manager as retail_summary_callback_manager
from callbacks.callbacks_pricing_input import callback_manager as pricing_input_callback_manager
from callbacks.callbacks_pricing_sales import callback_manager as prediction_output_callback_manager
from utility.utility_authentication import User, create_users_table

# SQL Alchemy DB instance to use it under models
db = SQLAlchemy()

# Create Db if it does not exists
conn = sqlite3.connect('data.sqlite')
engine = create_engine('sqlite:///data.sqlite')
users_tbl = Table('users', User.metadata)

# Normally Dash creates its own Flask server internally however
# by creating the server we can easily create routes for downloading files etc.
def create_app():
    dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
    external_stylesheets = [dbc.themes.BOOTSTRAP, dbc_css]
    server = Flask(__name__) 
    app = dash.Dash(external_stylesheets=external_stylesheets, server=server)
    app.config.suppress_callback_exceptions = True

    # DB configuration
    app.server.config.update(
        SECRET_KEY=os.urandom(12),
        SQLALCHEMY_DATABASE_URI='sqlite:///data.sqlite',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Instantiate db 
    db.init_app(app.server)

    # Instantiate Login Manager
    login_manager = LoginManager()
    login_manager.login_view = '/login'
    login_manager.init_app(app.server)

    # callback to reload the user object
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # create the user table in db
    create_users_table(engine)

    return app

app = create_app()

# Attaching tab based callbacks to app
authentication_callback_manager.attach_to_app(app)
sidepanel_callback_manager.attach_to_app(app)
retail_summary_callback_manager.attach_to_app(app)
pricing_input_callback_manager.attach_to_app(app)
prediction_output_callback_manager.attach_to_app(app)

# Adding log folder if it not exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Adding log handlers for simulator
logging.config.dictConfig(app_loggers)

'''
logger = logging.getLogger('pricing_handler')

# Segregating Dash Application Environment based on Configuration
if len(sys.argv)>1:
    if sys.argv[1] == "testing":
        print('Setting app config as Testing')
        app.server.config["ENV"] = "testing"
    elif sys.argv[1] == "development":
        print('Setting app config as Development')
        app.server.config["ENV"] = "development"
    elif sys.argv[1] == 'deployment':
        print('Setting app config as Deployment')
        app.server.config["ENV"] = "deployment"
    logger.info("Setting app config with %s Instance" %(sys.argv[1]))
'''

# Configuring Flask Server based on ENV type
if app.server.config["ENV"] == "production":
    print('Setting Production Configurations')
    app.server.config.from_object("config.appconfig.ProductionConfig")
    os.environ["ENV"] = "production"
elif app.server.config["ENV"] == "testing":
    print('Setting Testing Configurations')
    app.server.config.from_object("config.appconfig.TestingConfig")
    os.environ["ENV"] = "testing"
elif app.server.config["ENV"] == "development":
    print('Setting Development Configurations')
    app.server.config.from_object("config.appconfig.DevelopmentConfig")
    os.environ["ENV"] = "development"
else:
    print('Setting Deployment Configurations')
    app.server.config.from_object("config.appconfig.DeploymentConfig")
    os.environ["ENV"] = "deployment"