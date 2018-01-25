from flask_sqlalchemy import SQLAlchemy
from datetime import date

from main import app

db = SQLAlchemy(app)

class Bill(db.Model):
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

class Users(db.Model):
    username      = db.Column(db.String(100), primary_key=True)
    email         = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    admin         = db.Column(db.Boolean, nullable=False)

    def __init__(self, un, em, pw, ad):
        self.username = un
        self.email = em
        self.password_hash = pw
        self.admin = ad

    @staticmethod
    def add(username, email, password_hash, admin):
        new_user = User(username, email, password_hash, admin)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def delete(username):
        DB.db.session.delete(DB.Users.query.filter_by(username=username).first())
        DB.db.session.commit()
