from DB import db, User

db.create_all()

u = User('swat', 'swat@fk.fi', 'swat', True)
db.session.add(u)
db.session.commit()
