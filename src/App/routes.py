from flask import render_template, request
from App import app

import DB


@app.route('/', methods=['GET'])
def form():
    return render_template('form.html')


@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')


@app.route('/bills', methods=['GET'])
def bills_view():
    return render_template('view.html')


@app.route('/restore/<rid>', methods=['GET'])
def restore_view(rid):
    users = DB.User.query.filter_by(restore_id=rid).all()
    error = None
    if len(users) == 0:
        error = "IDtä ei löytynyt."
    return render_template('pwrestore.html', error=error)


@app.route('/restore/<rid>', methods=['POST'])
def restore(rid):
    json = request.get_json()
    users = DB.User.query.filter_by(restore_id=rid).all()
    if 'password' not in json or len(users) == 0:
        return "", 400
    return users[0].change_password(json['password'])


@app.route('/requestPasswordChange', methods=['GET'])
def request_password_change():
    return render_template('pwrequest.html')
