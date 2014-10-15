# -*- coding: utf-8 -*-

__author__ = 'novrain'

from apecoffee import db, app
from flask.ext.security import UserMixin, RoleMixin
import flask.ext.whooshalchemy as whooshalchemy

ROLE_ADMIN = 1
ROLE_VERSION = 2
ROLE_APP_VERSION = 3

ROLE_NAME_ADMIN = 'Admin'
ROLE_NAME_APP_VERSION = 'APPVM'
ROLE_NAME_VERSION = 'VM'


# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


STATUS_PLAN = 1
STATUS_BUILT = 2
STATUS_REBUILT = 3

TYPE_PUBLISH = 1
TYPE_INNER = 2
TYPE_TEST = 3
TYPE_CLOSED = 4

BIT_32 = 1
BIT_64 = 2
BIT_ALL = 3


class CommVersion(db.Model):
    """
    CommVersion
    """
    __searchable__ = {'version': 'text', 'desc': 'html', 'func': 'html', 'patch': 'html', 'date': 'text'}

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(64), index=True, unique=True)
    desc = db.Column(db.Text(4000))
    date = db.Column(db.Date)
    status = db.Column(db.SmallInteger, default=STATUS_PLAN)
    type = db.Column(db.SmallInteger, default=TYPE_PUBLISH)
    bit = db.Column(db.SmallInteger, default=BIT_ALL)
    func = db.Column(db.Text(8000))
    patch = db.Column(db.Text(9000))

    app_versions = db.relationship('AppVersion',
                                   cascade="all, delete-orphan",
                                   passive_deletes=True,
                                   lazy='dynamic')

    def __repr__(self):
        return '<%r>' % (self.version)


class AppVersion(db.Model):
    """
    AppVersion
    """
    __searchable__ = {'version': 'text', 'desc': 'html', 'date': 'text'}

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(64), index=True, unique=True)
    desc = db.Column(db.Text(4000))
    date = db.Column(db.Date)
    status = db.Column(db.SmallInteger, default=STATUS_BUILT)
    type = db.Column(db.SmallInteger, default=TYPE_PUBLISH)

    id_comm_version = db.Column(db.Integer,
                                db.ForeignKey('comm_version.id', ondelete='CASCADE'), nullable=False)

    comm_version = db.relationship('CommVersion')

    id_creator = db.Column(db.Integer,
                           db.ForeignKey('user.id', ondelete='CASCADE'))

    creator = db.relationship('User')

    def __repr__(self):
        return '<%r>' % (self.version)


whooshalchemy.whoosh_index(app, CommVersion)
whooshalchemy.whoosh_index(app, AppVersion)