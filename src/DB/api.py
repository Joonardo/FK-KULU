from flask_restless import APIManager
from DB import Bill, Receipt, User, db
from App import app
import Security

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(User,
                   methods=['GET', 'POST', 'DELETE'],
                   preprocessors={
                       'GET': [Security.auth],
                       'GET_MANY': [Security.auth],
                       'POST': [Security.auth],
                       'DELETE': [Security.auth, Security.requires_admin]
                   })

manager.create_api(Bill,
                   methods=['GET', 'POST'],
                   preprocessors={
                       'GET': [Security.auth],
                       'GET_MANY': [Security.auth],
                       'POST': [Bill.pre_post]
                   },
                   postprocessors={
                       'GET': [Bill.render]
                   })
