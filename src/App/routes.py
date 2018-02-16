from flask import render_template, request, url_for, redirect, make_response, send_from_directory
from schwifty import IBAN
import os
import random
import string
from functools import wraps

#from App.render import latexify
from App import app
import DB

@app.route('/', methods=['GET'])
def form():
    return render_template('form.html')

#@app.route('/', methods=['POST'])
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

@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')


@app.route('/bills', methods=['GET'])
def bills_view():
    return render_template('view.html')
