# -*- coding: utf-8 -*-

__author__ = 'novrain'

from apecoffee import app
from flask import render_template, redirect, url_for, request, g
from sqlalchemy import or_
from forms import CommVersionForm, AppVersionForm
from flask.ext.security import login_required, roles_accepted
from config import COUNT_PER_PAGE
from flask.ext.babel import gettext as _

from models import *


ACTIVE_COMM = 1
ACTIVE_APP = 2


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


'''
@app.route('/')
@app.route('/<int:type>')
@app.route('/<int:type>/<string:search>')
@app.route('/<int:type>/<string:search>/<int:page>')
@login_required
def index(type=None, search=None, page=None):
    if type is None:
        type = request.args.get('type')
    if search is None:
        search = request.args.get('search')
    if page is None and request.args.get('page') is not None:
        page = int(request.args.get('page'))
    else:
        page = 1

    versions = CommVersion.query
    if type is not None:
        versions = versions.filter(CommVersion.type == type)
    """
    if version is not None:
        versions = versions.filter(CommVersion.version.like('%' + version + '%'))
    """

    if search is not None:
        versions = versions.whoosh_search(search)
    versions = versions.order_by(CommVersion.date.desc()). \
        order_by(CommVersion.type.asc()). \
        paginate(page, COUNT_PER_PAGE, False)

    return render_template('commversion.html',
                           active=ACTIVE_COMM,
                           search=search,
                           type=type,
                           versions=versions)

'''

@app.route('/')
@app.route('/<int:type>')
@app.route('/<int:type>/<string:search>')
@app.route('/<int:type>/<string:search>/<int:page>')
def index(type=None, search=None, page=None):
    return render_template('index.html')


@app.route('/used')
@app.route('/used/<int:type>')
@app.route('/used/<int:type>/<string:search>')
@app.route('/used/<int:type>/<string:search>/<int:page>')
@login_required
def used(type=None, search=None, page=None):
    if type is None:
        type = request.args.get('type')
    if search is None:
        search = request.args.get('search')
    if page is None and request.args.get('page') is not None:
        page = int(request.args.get('page'))
    else:
        page = 1
    versions = AppVersion.query.join(CommVersion,
                                     (CommVersion.id == AppVersion.id_comm_version))
    if type is not None:
        versions = versions.filter(AppVersion.type == type)
    """
    if version is not None:
        versions = versions.filter(
            or_(CommVersion.version.like('%' + version + '%'),
                AppVersion.version.like('%' + version + '%')))
    """
    if search is not None:
        versions = versions.whoosh_search(search)
    if g.user is not None:
        versions = versions.filter(AppVersion.id_creator == g.user.id)

    versions = versions.order_by(AppVersion.date.desc()). \
        order_by(AppVersion.type.asc()). \
        paginate(page, COUNT_PER_PAGE, False)

    return render_template('used.html',
                           active=ACTIVE_APP,
                           type=type,
                           search=search,
                           versions=versions)


@app.route('/comm/new', methods=['GET', 'POST'])
@login_required
@roles_accepted(ROLE_NAME_ADMIN, ROLE_NAME_VERSION)
def comm_new():
    form = CommVersionForm()
    if form.validate_on_submit():
        exist = CommVersion.query.filter(CommVersion.version == form.version.data).first()
        if exist is not None:
            form.version.errors.append(_(u'该版本已存在.'))
            return render_template('comm_new.html',
                                   form=form,
                                   active=ACTIVE_COMM)
        commversion = CommVersion(version=form.version.data,
                                  desc=form.desc.data,
                                  type=form.type.data,
                                  date=form.date.data,
                                  func=form.func.data,
                                  patch=form.patch.data,
                                  bit=form.bit.data,
                                  status=form.status.data)
        db.session.add(commversion)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('comm_new.html',
                           form=form,
                           active=ACTIVE_COMM)


@app.route('/comm/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_accepted(ROLE_NAME_ADMIN, ROLE_NAME_VERSION)
def comm_edit(id):
    commversion = CommVersion.query.get(id)
    if commversion is None:
        return redirect(url_for('project'))
    form = CommVersionForm()
    if form.validate_on_submit():
        commversion.version = form.version.data
        commversion.desc = form.desc.data
        commversion.type = form.type.data
        commversion.date = form.date.data
        commversion.func = form.func.data
        commversion.patch = form.patch.data
        commversion.bit = form.bit.data
        commversion.status = form.status.data
        db.session.add(commversion)
        db.session.commit()
        return redirect(url_for('index'))

    if request.method != 'POST':
        form.version.data = commversion.version
        form.desc.data = commversion.desc
        form.type.data = commversion.type
        form.date.data = commversion.date
        form.func.data = commversion.func
        form.patch.data = commversion.patch
        form.bit.data = commversion.bit
        form.status.data = commversion.status
    return render_template('comm_edit.html',
                           form=form,
                           id=id,
                           active=ACTIVE_COMM)


@app.route('/comm/delete/<int:id>')
@roles_accepted(ROLE_NAME_ADMIN, ROLE_NAME_VERSION)
def comm_delete(id):
    commversion = CommVersion.query.get(id)
    if commversion:
        db.session.delete(commversion)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/app/new', methods=['GET', 'POST'])
@roles_accepted(ROLE_NAME_ADMIN, ROLE_NAME_APP_VERSION, ROLE_NAME_VERSION)
def app_new():
    form = AppVersionForm()
    form.comm.choices = [(comm.id, comm.version) for comm in CommVersion.query.order_by('date')]
    if form.validate_on_submit():
        id_creator = None
        if g.user is not None:
            id_creator = g.user.id
        exist = AppVersion.query.filter(AppVersion.version == form.version.data).first()
        if exist is not None:
            form.version.errors.append(_(u'该版本已存在.'))
            return render_template('app_new.html',
                                   form=form,
                                   active=ACTIVE_APP)
        appversion = AppVersion(version=form.version.data,
                                desc=form.desc.data,
                                type=form.type.data,
                                date=form.date.data,
                                status=form.status.data,
                                id_comm_version=form.comm.data,
                                id_creator=id_creator)
        db.session.add(appversion)
        db.session.commit()
        return redirect(url_for('used'))
    return render_template('app_new.html',
                           form=form,
                           active=ACTIVE_APP)


@app.route('/app/edit/<int:id>', methods=['GET', 'POST'])
@roles_accepted(ROLE_NAME_ADMIN, ROLE_NAME_APP_VERSION, ROLE_NAME_VERSION)
def app_edit(id):
    appversion = AppVersion.query.get(id)
    if appversion is None:
        return redirect(url_for('used'))
    if g.user is not None:
        if appversion.id_creator != g.user.id:
            return redirect(url_for('used'))
    form = AppVersionForm()
    form.comm.choices = [(comm.id, comm.version) for comm in CommVersion.query.order_by('date')]
    if form.validate_on_submit():
        appversion.version = form.version.data
        appversion.desc = form.desc.data
        appversion.type = form.type.data
        appversion.date = form.date.data
        appversion.status = form.status.data
        appversion.id_comm_version = form.comm.data
        db.session.add(appversion)
        db.session.commit()
        return redirect(url_for('used'))

    if request.method != 'POST':
        form.version.data = appversion.version
        form.desc.data = appversion.desc
        form.type.data = appversion.type
        form.date.data = appversion.date
        form.status.data = appversion.status
        form.comm.data = appversion.id_comm_version
    return render_template('app_edit.html',
                           form=form,
                           id=id,
                           active=ACTIVE_APP)


@app.route('/app/delete/<int:id>')
@roles_accepted(ROLE_NAME_ADMIN, ROLE_NAME_APP_VERSION, ROLE_NAME_VERSION)
def app_delete(id):
    appversion = AppVersion.query.get(id)
    if appversion is not None:
        if g.user is not None:
            if appversion.id_creator != g.user.id:
                return redirect(url_for('used'))
        db.session.delete(appversion)
        db.session.commit()
    return redirect(url_for('used'))