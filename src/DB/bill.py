from DB import db
from datetime import date

class Bill(db.Model):
    __tablename__ = 'bills'
    id = db.Column(db.Integer, primary_key=True)
    submitter = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    filename = db.Column(db.String(50), nullable=False, unique=True)
    accepted = db.Column(db.Boolean, default=False, nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, submitter, filename):
        self.submitter = submitter
        self.filename = filename
        self.date = str(date.today())
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def all():
        return Bill.query.all()

    @staticmethod
    def accept(bid):
        bill = Bill.query.get(bid)
        bill.accepted = True
        db.session.add(bill)
        db.session.commit()

    @staticmethod
    def pretty_name(fn):
        bill = Bill.query.filter_by(filename=fn).first()
        return "{}-{}.pdf".format(bill.submitter.replace(" ", "_"), bill.date)
