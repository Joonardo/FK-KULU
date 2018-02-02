from DB import db
from hashlib import sha512
from binascii import a2b_base64
from App import app

class Receipt(db.Model):
    __tablename__ = 'receipts'
    id = db.Column(db.Integer, primary_key=True)
    kuvaus = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(128), nullable=False)
    summa = db.Column(db.Float, nullable=False)

    def __init__(self, summa, kuvaus, tiedosto):
        self.kuvaus = kuvaus
        self.summa = summa

        data = a2b_base64(tiedosto)
        self.filename = sha512(data).hexdigest()

        with open(app.config['RECEIPTS_FOLDER'] + self.filename, 'wb') as f:
            f.write(data)

        db.session.add(self)
