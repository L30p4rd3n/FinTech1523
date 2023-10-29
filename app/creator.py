import app
from app import User, db
with app.app_context():
    zero = User(email = 'test@@', password = 'abc', name = 'asda')
    db.session.add(zero)
    db.session.commit()