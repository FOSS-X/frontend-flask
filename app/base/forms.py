# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField, BooleanField, FormField, FieldList
from wtforms.validators import InputRequired, Email, DataRequired

## login and registration


class LoginForm(FlaskForm):
    username = TextField('Username', id='username_login', validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login', validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = TextField('Username', id='username_create', validators=[DataRequired()])
    email = TextField('Email', id='email_create', validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='pwd_create', validators=[DataRequired()])
    repeat_password = PasswordField(
        'Repeat Password', id='rpwd_create', validators=[DataRequired()])


class ResetPasswordForm(FlaskForm):
    email = TextField('Email', id='email_create', validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='pwd_create', validators=[DataRequired()])
    repeat_password = PasswordField(
        'Repeat Password', id='rpwd_create', validators=[DataRequired()])


class CreateDatabaseForm(FlaskForm):
    database_type = SelectField(u'Database Type', choices=[(
        'mysql', "MySQL"), ("mongodb", "MongoDB")], id="database_type", validators=[DataRequired()])
    database_name = TextField('Database Name', id='database_name_create',
                              validators=[DataRequired()])


class AttributeForm(FlaskForm):
    attribute_name = TextField('Attribute Name', id="attribute_name_create",
                               validators=[DataRequired()])
    datatype = SelectField(u'DataType', choices=[(
        'int', "Integer"), ("VARCHAR(256)", "String"), ("BOOLEAN", "Boolean"), ("DOUBLE", "Double"), ("DATE", "Date"), ("TIME", "Time"), ("DATETIME", "Date Time")], id="database_type", validators=[DataRequired()])
    pk = BooleanField('PK', validators=[DataRequired()])
    nn = BooleanField('NN', validators=[DataRequired()])
    ai = BooleanField('AI', validators=[DataRequired()])


class CreateEntitySetForm(FlaskForm):
    entity_set_name = TextField(
        'Entity Set Name', id='entity_set_name_create', validators=[DataRequired()])
    attributes = FieldList('attributes', FormField(AttributeForm))
