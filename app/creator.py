from app import app, db, User
with app.app_context():
    db.create_all()
    User.name = "asda"
    db.session.commit()