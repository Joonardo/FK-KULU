from flask_sqlalchemy import SQLAlchemy

from App import app
db = SQLAlchemy(app)

from .user import User
from .bill import Bill
from .receipt import Receipt
from .api import *
