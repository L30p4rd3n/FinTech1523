from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired

class LoginForm(Form):
    # openid = StringField('openid', validators = [DataRequired()])
    #remember_me = BooleanField('Remember this name', default=False)
    a = StringField()
