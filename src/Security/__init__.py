from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired
from flask import g
from flask_restless import ProcessingException

from DB import User
from App import app
from .password import verify

ser = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_in=3600)

def auth(**kw):
    try:
        data = ser.loads(kw['data']['token'])
    except BadSignature:
        raise ProcessingException(description='Oops, something went wrong with your token...')
    except SignatureExpired:
        raise ProcessingException(description='Your token has expired.', code=400)

    del kw['data']['token'] # Is this necessary?
    g.user = User.query.filter_by(username=data['username'])

def get_auth_token(**kw):
    user = User.query.filter_by(username=kw['data']['username']).one()

    if verify(kw['data']['password'], user.password_hash):
        return ser.dump({'username': user.username})

    raise ProcessingException(description='Wrong password or username.')
