from DB import db
import Security.password as pw

class User(db.Model):
    __tablename__ = 'users'
    username      = db.Column(db.String(100), primary_key=True)
    email         = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    admin         = db.Column(db.Boolean, nullable=False)

    @staticmethod
    def preprocess(**kw):
        kw['data']['password_hash'] = pw.hash(kw['data']['password'])
        del kw['data']['password']
