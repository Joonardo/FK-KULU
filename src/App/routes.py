from flask import render_template
from App import app


@app.route('/', methods=['GET'])
def form():
    return render_template('form.html')


@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')


@app.route('/bills', methods=['GET'])
def bills_view():
    return render_template('view.html')
