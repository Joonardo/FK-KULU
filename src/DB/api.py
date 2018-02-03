from flask_restless import APIManager
from DB import Bill, Receipt, User, db
from App import app

def pre(**kw):
    print('PRE: ' + str(kw))

def post(**kw):
    print('POST: ' + str(kw))

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(User, methods=['GET', 'POST', 'DELETE'], preprocessors={'GET_MANY': [pre], 'POST': [pre]})
manager.create_api(Bill,
                   methods=['GET', 'POST'],
                   #include_columns=['id', 'submitter', 'iban', 'description', 'receipts.content', 'receipts.description', 'receipts.amount'],
                   preprocessors={'GET_MANY': [pre], 'POST': [Bill.pre_post]},
                   postprocessors={'GET_MANY': [post], 'POST': [post]})
