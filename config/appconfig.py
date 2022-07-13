__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import os
import json

config_data_snowflakes, config_model_endpoints, config_model_picklefiles = None, None, None

try:
    if os.path.exists(os.path.join('config','config_snowflakes.json')):
        with open(os.path.join('config','config_snowflakes.json')) as config_file:
            config_data_snowflakes = json.load(config_file)
except Exception as ex:
    print("Reading Snowflakes Configuration raised an exception: "+str(ex))

try:
    if os.path.exists(os.path.join('config','config_modelendpoints.json')):
        with open(os.path.join('config','config_modelendpoints.json')) as config_file:
            config_model_endpoints = json.load(config_file)
except Exception as ex:
    print("Reading Model Endpoint Configuration raised an exception: "+str(ex))

try:
    if os.path.exists(os.path.join('config','config_modelpicklefiles.json')):
        with open(os.path.join('config','config_modelpicklefiles.json')) as config_file:
            config_model_picklefiles = json.load(config_file)
except Exception as ex:
    print("Reading Model Pickle Configuration raised an exception: "+str(ex))

class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    SNOWFLAKE_LOGIN_CREDENTIALS_OUTBOUND = config_data_snowflakes["login_outbound"]["login_credentials_generic"] if config_data_snowflakes is not None else {}
    SNOWFLAKE_LOGIN_CREDENTIALS_RAW = config_data_snowflakes["login_raw"]["login_credentials_generic"] if config_data_snowflakes is not None else {}
    SNOWFLAKE_LOGIN_CREDENTIALS_INTEGRATION = config_data_snowflakes["login_integration"]["login_credentials_generic"] if config_data_snowflakes is not None else {}
    PRICING_MODEL_ENDPOINTS = config_model_endpoints if config_model_endpoints is not None else {}
    PRICING_MODEL_PKLFILES = config_model_picklefiles if config_model_picklefiles is not None else {}
    
class TestingConfig(Config):
    TESTING = True

class DevelopmentConfig(Config):
    DEBUG = True

class DeploymentConfig(Config):
    SNOWFLAKE_LOGIN_CREDENTIALS_OUTBOUND = config_data_snowflakes["login_outbound"]["login_credentials_deployment"] if config_data_snowflakes is not None else {}
    SNOWFLAKE_LOGIN_CREDENTIALS_RAW = config_data_snowflakes["login_raw"]["login_credentials_deployment"] if config_data_snowflakes is not None else {}
    SNOWFLAKE_LOGIN_CREDENTIALS_INTEGRATION = config_data_snowflakes["login_integration"]["login_credentials_deployment"] if config_data_snowflakes is not None else {}
    PRICING_MODEL_ENDPOINTS = config_model_endpoints if config_model_endpoints is not None else {}
    PRICING_MODEL_PKLFILES = config_model_picklefiles if config_model_picklefiles is not None else {}