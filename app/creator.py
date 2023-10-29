from app import db, create_app


def create_user(app):
    with app.app_context():
        import models
        db.session.add(models.User)
        db.commit()
    return "asda"

app = create_app()
create_user(app=app)
