from DB import db
from App import app
from .receipt import Receipt
from datetime import datetime
from .render import latexify

from flask_restless import ProcessingException
from schwifty import IBAN
from flask import send_from_directory

class Bill(db.Model):
    __tablename__ = 'bills'
    id = db.Column(db.Integer, primary_key=True)
    submitter = db.Column(db.String(40), nullable=False)
    iban = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    #receipts = db.relationship('Receipt', backref='bill', lazy=True)

    #def __init__(self, submitter, iban, description, receipts):
    #    self.submitter = submitter
    #    self.date = datetime.now()
    #    self.iban = iban
    #    self.description = description
    #    self.receipts = receipts
    #
    #    for r in receipts:
    #        r.bill = self
    #        db.session.add(r)
    #
    #    db.session.add(self)
    #    db.session.commit()

    # Preprocessor for posting new bill
    @staticmethod
    def pre_post(**kw):

        submitter = kw['data']['submitter']
        iban = kw['data']['iban']
        description = kw['data']['description']
        receipts = kw['data']['receipts']

        kw['data']['date'] = str(datetime.now())

        errors = []

        if len(submitter or '\0') == 0:
            errors.append('Nimi on pakollinen kenttä.')

        try:
            IBAN(iban or '\0')
        except ValueError:
            errors.append('IBAN ei ole validi.')

        if len(description or '\0') == 0:
            errors.append('Maksun peruste tulee antaa.')

        if len(receipts) == 0:
            errors.append('Tositteita ei löytynyt.')

        if len(errors) > 0:
            raise ProcessingException(description='\n'.join(errors))

        for r in receipts:
            Receipt.check(**r)

        nrs = []
        for r in receipts:
            nrs.append(Receipt.preprocess(**r))
        kw['data']['receipts'] = nrs

        print(kw['data'])

    @staticmethod
    def render(id):
        fn = latexify(Bill.query.get(id))
        if not fn:
            return "Oops...", 404

        return send_from_directory(app.config['TMP_FOLDER'], fn, as_attachment=True)

    @staticmethod
    def pretty_name(fn):
        bill = Bill.query.filter_by(filename=fn).first()
        return "{}-{}.pdf".format(bill.submitter.replace(" ", "_"), bill.date)
