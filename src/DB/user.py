from DB import db

class User(db.Model):
    __tablename__ = 'users'
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
        db.session.delete(DB.Users.query.filter_by(username=username).first())
        db.session.commit()
