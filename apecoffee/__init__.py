# -*- coding: utf-8 -*-

__author__ = 'novrain'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.mail import Mail
from flask.ext.security import Security, SQLAlchemyUserDatastore


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
babel = Babel(app)
mail = Mail(app)

app.debug = True

toolbar = DebugToolbarExtension(app)

from apecoffee import models
from apecoffee import views

from sqlalchemy.engine import Engine
from sqlalchemy import event

from apecoffee.models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from apecoffee import login_views

# Sqlite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()