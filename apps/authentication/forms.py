# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired

# login and registration


class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class DoctorAccountForm(FlaskForm):
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    nama = StringField('Nama',
                         id='Nama_create',
                         validators=[DataRequired()])
    nik = StringField('Nik',
                         id='Nik_create',
                         validators=[DataRequired()])
    no_str = StringField('No_str',
                         id='No_str_create',
                         validators=[DataRequired()])
    alamat = StringField('Alamat',
                         id='Alamat_create',
                         validators=[DataRequired()])

class DoctorProfileForm(FlaskForm):
    nama = StringField('Nama',
                         id='Nama_create',
                         validators=[DataRequired()])
    nik = StringField('Nik',
                         id='Nik_create',
                         validators=[DataRequired()])
    no_str = StringField('No_str',
                         id='No_str_create',
                         validators=[DataRequired()])
    alamat = StringField('Alamat',
                         id='Alamat_create',
                         validators=[DataRequired()])
