# -*- coding: utf-8 -*-

__author__ = 'novrain'

from apecoffee import app, db, user_datastore
from flask import g
from flask.ext.security import current_user, user_registered
from models import ROLE_NAME_APP_VERSION


@app.before_request
def before_request():
    g.user = current_user


@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
    default_role = user_datastore.find_role(ROLE_NAME_APP_VERSION)
    #default_role = Role.query.filter_by(id=ROLE_NAME_APP_VERSION).first()
    user_datastore.add_role_to_user(user, default_role)
    db.session.commit()
