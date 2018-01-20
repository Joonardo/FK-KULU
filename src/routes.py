from flask import render_template, request, url_for, redirect, make_response, send_from_directory
from schwifty import IBAN
import os
from functools import wraps

from render import latexify
from app import app
import DB

def auth_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != app.config['USER'] or auth.password != app.config['PASSWORD']:
            return "Kirjaudu sisään.", 401, {'WWW-Authenticate': 'Basic realm="Sisäänkirjautuminen vaaditaan."'}
        return f(*args, **kwargs)
    return wrapped

@app.route('/', methods=['GET'])
def form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def receive():
    errors = []
    bill = {}

    if len(request.form.get('nimi', '\0')) == 0:
        errors.append('Nimi on pakollinen kenttä.')

    try:
        IBAN(request.form.get('iban', '\0'))
    except ValueError:
        errors.append('IBAN ei ole validi.')

    if len(request.form.get('peruste', '\0')) == 0:
        errors.append('Maksun peruste tulee antaa.')

    if len(request.form.get('ids', '\0')) == 0:
        errors.append('Tositteita ei löytynyt.')

    if len(errors) > 0:
        return '\n'.join(errors), 400

    bill['nimi'] = request.form['nimi']
    bill['iban'] = request.form['iban']
    bill['peruste'] = request.form['peruste']
    bill['tositteet'] = []

    ids = request.form.get('ids', '\0').split(',')
    for id in ids:
        kuvaus = "kuvaus" + id
        liite = "liite" + id
        summa = "summa" + id

        if (not kuvaus in request.form) or (not summa in request.form) or (not liite in request.files):
            return 'Liiteistä puuttuu tietoja.', 400

        bill['tositteet'].append({
                'kuvaus': request.form[kuvaus],
                'liite': request.files[liite],
                'summa': request.form[summa]
            })

    retf = latexify(**bill)

    if not retf:
        return 'Kääntäminen epäonnistui.', 400

    DB.Bill(bill['nimi'], retf)

    return 'Lähettäminen onnistui.', 200

@app.route('/bills', methods=['GET'])
@auth_required
def view():
    return render_template('view.html', bills=DB.Bill.all())

@app.route('/bills/<filename>', methods=['GET'])
@auth_required
def download(filename):
    print(os.getcwd())
    return send_from_directory(os.getcwd() + '/bills', filename, as_attachment=True, attachment_filename=DB.Bill.pretty_name(filename))