from DB import db
import Security.password as pw

class User(db.Model):
    __tablename__ = 'users'
    username      = db.Column(db.String(100), primary_key=True)
    email         = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    admin         = db.Column(db.Boolean, nullable=False)

    def __init__(self, username, email, password, admin):
        self.username = username
        self.email = email
        self.password_hash = pw.hash(password)
        self.admin = admin
