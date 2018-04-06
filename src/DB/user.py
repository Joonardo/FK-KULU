from DB import db
from uuid import uuid4
from datetime import datetime, timedelta
import Security.password as pw


class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(100), primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    restore_id = db.Column(db.Text, unique=True)
    restore_valid = db.Column(db.DateTime)

    def change_password(self, pw):
        if not self.restore_valid or datetime.now() > self.restore_valid:
            return "", 400
        self.password_hash = pw.hash(pw)
        self.restore_id = None
        self.restore_valid = None
        db.session.add(self)
        db.session.commit()
        return "", 200

    def request_password_change(self):
        self.restore_id = str(uuid4())
        self.restore_valid = datetime.now() + timedelta(days=1)
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def preprocess(**kw):
        kw['data']['password_hash'] = pw.hash(kw['data']['password'])
        del kw['data']['password']
