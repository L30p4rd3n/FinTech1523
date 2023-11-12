from flask import Flask
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aGRjZmRzNDIzMzRmc2QzNDemZnMTIzZGY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hella_db.sqlite'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    UserAttrib = db.Column(db.Integer)  # could possibly be changed to a list of links??
    # how 'bout making a separate database to take the links from for filling?


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from app.auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

