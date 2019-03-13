from flask_wtf import FlaskForm
from wtforms import PasswordField, TextField, StringField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

## login and registration


class LoginForm(FlaskForm):
    email = TextField('email', id='username_login')
    password = PasswordField('Password', id='pwd_login')


class CreateAccountForm(FlaskForm):
    email = TextField('Email', id='email_create')
    first_name=TextField('First Name', id='firstname_create')
    last_name=TextField('last_name', id='lastname_create')
    company=TextField('company', id='company_create')
    password = PasswordField('Password', id='pwd_create', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')


class SubmitMessage(FlaskForm):
    name = TextField('Name', id='name_create')
    email = TextField('Email', id='email_create')
    subject = TextField('Subject', id='subject_create')
    message = TextField('Message', id='message_create')
    