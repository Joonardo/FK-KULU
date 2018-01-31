from flask_restless import APIManager
from DB import Bill, User, db
from App import app

manager = APIManager.create_api(app, flask_sqlalchemy_db=db, url_prefix='/api')

manager.create_api(User, endpoints=['GET', 'POST', 'DELETE'])
manager.create_api(Bill, endpoints=['GET', 'POST'])
