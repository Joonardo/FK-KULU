from DB import db
from .user import User
from hashlib import sha512
from binascii import a2b_base64
from App import app
from flask_restless import ProcessingException

class Receipt(db.Model):
    __tablename__ = 'receipts'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id'), nullable=False)

    def __init__(self, description, amount, content):

        if (not description) or (not amount) or (not content):
            raise ProcessingException(description='Tositteista puuttuu tietoja.')

        self.description = description
        self.amount = amount

        header, data = content.split(',')
        data = a2b_base64(data)
        type = header.split('/')[1].split(';')[0]
        self.filename = sha512(data).hexdigest() + '.pdf'

        with open(app.config['RECEIPTS_FOLDER'] + self.filename, 'wb') as f:
            f.write(data)
