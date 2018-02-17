from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired
from flask import g, request
from flask_restless import ProcessingException

from Security.password import verify
from App import app
from DB import User

ser = TimedJSONWebSignatureSerializer(app.config['SECRET'], expires_in=3600)

def auth(**kw):
    if not 'auth' in request.headers:
        raise ProcessingException(description='Unauthorized.')
    try:
        data = ser.loads(request.headers['auth'].encode('ascii'))
    except BadSignature:
        raise ProcessingException(description='Oops, something went wrong with your token...')
    except SignatureExpired:
        raise ProcessingException(description='Your token has expired.', code=400)

    g.user = User.query.filter_by(username=data['username']).first()

def get_auth_token(username, password):
    user = User.query.filter_by(username=username).first()

    if not user:
        return ['User not found.', '']

    if verify(password, user.password_hash):
        print(user.username)
        return ['Success', ser.dumps({'username': user.username}).decode('ascii')]

    return ['Wrong password or username.', '']

def requires_admin(**kw):
    print(kw)
    if not g.user.admin:
        raise ProcessingException(description='Only admin can do this.')
