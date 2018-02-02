from flask_restless import APIManager
from DB import Bill, User, db
from App import app

def pre(**kw):
    print(kw)

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(User, methods=['GET', 'POST', 'DELETE'], preprocessors={'GET_MANY': [pre], 'POST': [pre]})
manager.create_api(Bill, methods=['GET', 'POST'], preprocessors={'GET_MANY': [pre], 'POST': [pre]})
