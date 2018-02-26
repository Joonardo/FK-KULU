from DB import Bill, User, db
from Security.password import hash

from datetime import datetime, timedelta

for i in range(100):
    bill = Bill(
        submitter="Loers The {}".format(i),
        description="Kaljaa {}".format(i),
        iban="DE79850503003100180568",
        date=datetime.now() + timedelta(days=-i),
        receipts=[]
    )
    db.session.add(bill)

uns = ['Rahis', 'Puhis', 'IE', 'Äbäj']

for un in uns:
    user = User(
        username=un,
        password_hash=hash(un),
        admin=False
    )

db.session.commit()
