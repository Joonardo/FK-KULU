import sys
from DB import db, User
from Security import password

if 'y' != input('Tämä tuohoaa tietokannan, oletko varma? [y/n]'):
    sys.exit()


db.drop_all()
db.create_all()

u = User()
u.username = 'swat'
u.password_hash = password.hash('swat')
u.email = 'swat@fk.fi'
u.admin = True

db.session.add(u)
db.session.commit()
