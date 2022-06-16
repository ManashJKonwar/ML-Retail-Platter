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
import logging, logging.config
import dash_bootstrap_components as dbc
from flask import Flask
from callbacks.callbacks_sidepanel import callback_manager as sidepanel_callback_manager
# from config.applogger import LOGGING
# from callbacks.callbacks_pricing_input import callback_manager as pricing_input_cm

# Normally Dash creates its own Flask server internally however
# by creating the server we can easily create routes for downloading files etc.
external_stylesheets = [dbc.themes.BOOTSTRAP]
server = Flask(__name__) 
app = dash.Dash(external_stylesheets=external_stylesheets, server=server)
app.config.suppress_callback_exceptions = True

# Attaching tab based callbacks to app
sidepanel_callback_manager.attach_to_app(app)

'''
# Adding log folder if it not exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Adding Log handlers for Simulator
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('pricing_handler')

pricing_input_cm.attach_to_app(app)

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
'''