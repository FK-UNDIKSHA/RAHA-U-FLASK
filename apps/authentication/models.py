# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import datetime

from flask_login import UserMixin

from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True)
    email         = db.Column(db.String(64), unique=True)
    password      = db.Column(db.LargeBinary)
    role          = db.relationship('Roles', secondary='user_roles')

    oauth_github  = db.Column(db.String(100), nullable=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    @classmethod
    def find_by_email(cls, email: str) -> "Users":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username: str) -> "Users":
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, _id: int) -> "Users":
        return cls.query.filter_by(id=_id).first()
   
    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
          
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
    
    def delete_from_db(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return

class Roles(db.Model):
    __tablename__ = 'roles'

    id              = db.Column(db.Integer, primary_key=True)
    role            = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return str(self.role)


class Dokter(db.Model):
    __tablename__ = 'dokter'

    id              = db.Column(db.Integer, primary_key=True)
    nama            = db.Column(db.Text(16000000), unique=True)
    username        = db.Column(db.Text(255), unique=True)
    nik             = db.Column(db.String(255), unique=True)
    no_str          = db.Column(db.String(255), unique=True)
    alamat          = db.Column(db.Text(16000000))
    no_hp           = db.Column(db.String(255))
    imaji           = db.Column(db.Text(16000000))
    created_at      = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return str(self.username)


class Pengguna(db.Model):
    __tablename__ = 'pengguna'

    id              = db.Column(db.Integer, primary_key=True)
    nama            = db.Column(db.Text(16000000), unique=True)
    username        = db.Column(db.Text(255), unique=True)
    nik             = db.Column(db.String(255), unique=True)
    #no_str          = db.Column(db.String(255), unique=True)
    no_hp           = db.Column(db.String(255))
    alamat          = db.Column(db.Text(16000000))
    imaji           = db.Column(db.Text(16000000))
    created_at      = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return str(self.role)

#Tabel Relasi
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None

class OAuth(OAuthConsumerMixin, db.Model):
    #Many to one relation?
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"), nullable=False)
    user = db.relationship(Users)
