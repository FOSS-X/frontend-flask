# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, DataRequired

## login and registration

class LoginForm(FlaskForm):
    username = TextField    ('Username', id='username_login'   , validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    username        = TextField('Username'     , id='username_create' , validators=[DataRequired()])
    email           = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    password        = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', id='rpwd_create'     , validators=[DataRequired()])

class ResetPasswordForm(FlaskForm):
    email           = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    password        = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', id='rpwd_create'     , validators=[DataRequired()])

class CreateDatabaseForm(FlaskForm):
    database_type = SelectField(u'Database Type', choices=[('',"--Database Type--"),('mysql',"MySQL"),("mongodb","MongoDB")], id="database_type", validators=[DataRequired()])
    database_name=TextField('Database Name'     , id='database_name_create' , validators=[DataRequired()])
