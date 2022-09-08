__author__ = "konwar.m"
__copyright__ = "Copyright 2022, AI R&D"
__credits__ = ["konwar.m"]
__license__ = "Individual Ownership"
__version__ = "1.0.1"
__maintainer__ = "konwar.m"
__email__ = "rickykonwar@gmail.com"
__status__ = "Development"

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

#region Task Class
class Task(UserMixin, db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    taskid = db.Column(db.String(50), unique=True, nullable=False)
    taskstatus = db.Column(db.String(15), nullable=False)
    scenarioname = db.Column(db.String(15), nullable=False)
    submissiondate = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Task {}>'.format(self.taskid)

# Function to create a specific task
def create_tasks_table(engine):
    Task.metadata.create_all(engine)
#endregion