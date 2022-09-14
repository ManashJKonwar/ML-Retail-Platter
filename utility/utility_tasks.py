__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

#region Task Class
class Task(UserMixin, db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), nullable=False)
    dbtaskid = db.Column(db.String(50), nullable=False)
    taskid = db.Column(db.String(50))
    taskdata = db.Column(db.LargeBinary)
    taskstatus = db.Column(db.String(15))
    scenarioname = db.Column(db.String(15), nullable=False)
    submissiondate = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Task {}>'.format(self.id)

# Function to create a specific task
def create_tasks_table(engine):
    Task.metadata.create_all(engine)
#endregion

#region Task Upload Model
class TaskUploadModel:
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self._var_object = {} # Includes floats and integers
        self._df_object = {} # Includes dataframes
        self._list_object = {} # Includes lists
        self._dict_object = {} # Includes dicts
        self._extract_items()

    def _extract_items(self):
        for k in self._kwargs.keys():
            if isinstance(self._kwargs[k], int) or isinstance(self._kwargs[k], float) or isinstance(self._kwargs[k], str):
                self._var_object[k] = self._kwargs[k]
            elif isinstance(self._kwargs[k], pd.DataFrame):
                self._df_object[k] = self._kwargs[k]
            elif isinstance(self._kwargs[k], dict):
                self._dict_object[k] = self._kwargs[k]
            elif isinstance(self._kwargs[k], list):
                self._list_object[k] = self._kwargs[k]

    def upload_files(self):
        print('here')
        return True
    
    def convert_to_blob(self):
        print('here')
        return True
    
    def generate_json(self):
        print('here')
#endregion