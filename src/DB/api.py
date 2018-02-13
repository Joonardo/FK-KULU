from flask_restless import APIManager
from flaks import jsonify

from DB import Bill, Receipt, User, db
from App import app
import Security.token as sec

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(User,
                   methods=['GET', 'POST', 'DELETE'],
                   preprocessors={
                       'GET': [sec.auth],
                       'GET_MANY': [sec.auth],
                       'POST': [sec.auth],
                       'DELETE': [sec.auth, sec.requires_admin]
                   })

manager.create_api(Bill,
                   methods=['GET', 'POST'],
                   preprocessors={
                       'GET': [sec.auth],
                       'GET_MANY': [sec.auth],
                       'POST': [Bill.pre_post]
                   })


@app.route('/api/bills/<id>/pdf', methods=['GET'])
def download(id):
    pass
