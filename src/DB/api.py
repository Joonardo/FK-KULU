from flask_restless import APIManager, ProcessingException
from flask import jsonify, request

from DB import Bill, User, db
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
                   }
                   # exclude_columns=['receipts']
                   )


@app.route('/api/pdf/<id>', methods=['GET'])
def download(id):
    try:
        sec.auth()
    except ProcessingException:
        return 'Oops, you are not allowed to do that.', 400
    return Bill.render(id)


@app.route('/api/accept/<id>', methods=['POST'])
def accept(id):
    try:
        sec.auth()
    except ProcessingException:
        return 'Oops, you are not allowed to do that.', 400
    data = request.get_json()
    if not data or 'description' not in data or data['description'] == "":
        return "", 400
    Bill.accept(id, data['description'], data['paidDesc'])
    return "", 200


@app.route('/api/toggleHide/<id>', methods=['POST'])
def toggle_hide(id):
    try:
        sec.auth()
    except ProcessingException:
        return 'Oops, you are not allowed to do that.', 400
    Bill.toggle_hidden(id)
    return "", 200


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return '', 400
    message, token = sec.get_auth_token(data['username'], data['password'])
    return jsonify({'message': message, 'token': token})


@app.route('/api/requestPasswordChange', methods=["POST"])
def request_password_change_api():
    json = request.get_json()
    if 'email' not in json:
        return "", 400
    users = User.query.filter_by(email=json['email']).all()
    if len(users) == 0:
        return "", 400

    users[0].request_password_change()

    return "", 200
