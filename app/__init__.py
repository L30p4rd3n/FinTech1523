from flask import Flask, render_template, redirect, request, url_for, current_app, flash
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'qwert'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hella_db.sqlite'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    #from app.models import User

    #@login_manager.user_loader
    #def load_user(user_id):
    #    return User.query.get(user_id)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

