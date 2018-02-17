from flask_restless import APIManager, ProcessingException
from flask import jsonify, request, make_response

from DB import Bill, Receipt, User, db
from App import app
import Security.token as sec

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(User,
                   methods=['GET', 'POST', 'DELETE'],
                   preprocessors={
                       'GET': [sec.auth],
                       'GET_MANY': [sec.auth],
                       'POST': [sec.auth, sec.requires_admin, User.preprocess],
                       'DELETE_SINGLE': [sec.auth, sec.requires_admin]
                   },
                   exclude_columns=['password_hash']
                   )

manager.create_api(Bill,
                   methods=['GET', 'POST'],
                   preprocessors={
                       'GET': [sec.auth],
                       'GET_MANY': [sec.auth],
                       'POST': [Bill.preprocess_post]
                   },
                   exclude_columns=['receipts']
                   )

@app.route('/api/bills/<id>/pdf', methods=['GET'])
def download(id):
    try:
        sec.auth()
    except ProcessingException:
        return 'Oops, you are not allowed to do that.', 400
    return Bill.render(id)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return '', 400
    message, token = sec.get_auth_token(data['username'], data['password'])
    return jsonify({'message': message, 'token': token})
