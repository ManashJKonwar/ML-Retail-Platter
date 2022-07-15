__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import os 

app_loggers = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s - %(funcName)s()] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'pricing_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join('logs', 'simulator.log'),
            'when': 'D', # this specifies the interval
            'interval': 1, # defaults to 1, only necessary for other values 
            'backupCount': 10, # how many backup file to keep, 10 days
            'formatter': 'verbose',
        },
        'baseprediction_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join('logs', 'baseline.log'),
            'when': 'D', # this specifies the interval
            'interval': 1, # defaults to 1, only necessary for other values 
            'backupCount': 10, # how many backup file to keep, 10 days
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'pricing_handler': {
            'handlers': ['pricing_handler'],
            'level': 'INFO',
        },
        'baseprediction_handler': {
            'handlers': ['baseprediction_handler'],
            'level': 'INFO',
        }
    }
}