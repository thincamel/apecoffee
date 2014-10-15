# -*- coding: utf-8 -*-

__author__ = 'novrain'

import datetime
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import Required
from models import *
from flask.ext.babel import gettext as _

STATUS_CHOICES = [(STATUS_PLAN, _(u"待制作")),
                  (STATUS_BUILT, _(u"已制作")),
                  (STATUS_REBUILT, _(u"其他"))];

TYPE_CHOICES = [(TYPE_PUBLISH, _(u"对外发布")),
                (TYPE_INNER, _(u"对内发布")),
                (TYPE_TEST, _(u"测试版本")),
                (TYPE_CLOSED, _(u"其他"))];

BIT_CHOICES = [(BIT_ALL, _(u"32&64")),
               (BIT_64, _(u"64")),
               (BIT_32, _(u"32"))];


class CHRequired(Required):
    def __init__(self):
        Required.__init__(self, _(u'该信息不能为空.'))


class CHDateField(DateTimeField):
    """
    Same as DateTimeField, except stores a `datetime.date`.
    """

    def __init__(self, label=None, validators=None, format='%Y-%m-%d', **kwargs):
        super(CHDateField, self).__init__(label, validators, format, **kwargs)

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                self.data = datetime.datetime.strptime(date_str, self.format).date()
            except ValueError:
                self.data = None
                raise ValueError(_(u'日期格式非法.'))


class CommVersionForm(Form):
    version = TextField('name', validators=[CHRequired()])
    desc = TextAreaField('desc')
    date = CHDateField('date', format='%Y-%m-%d')
    status = SelectField('status', coerce=int, validators=[CHRequired()],
                         choices=STATUS_CHOICES, default=STATUS_PLAN)
    type = SelectField('type', coerce=int, validators=[CHRequired()],
                       choices=TYPE_CHOICES, default=TYPE_PUBLISH)
    bit = SelectField('bit', coerce=int, validators=[CHRequired()],
                      choices=BIT_CHOICES, default=BIT_ALL)
    func = TextAreaField('func')
    patch = TextAreaField('patch')


class AppVersionForm(Form):
    version = TextField('name', validators=[CHRequired()])
    desc = TextAreaField('desc')
    date = CHDateField('date', format='%Y-%m-%d')
    status = SelectField('status', coerce=int, validators=[CHRequired()],
                         choices=STATUS_CHOICES, default=STATUS_PLAN)
    type = SelectField('type', coerce=int, validators=[CHRequired()],
                       choices=TYPE_CHOICES, default=TYPE_PUBLISH)
    comm = SelectField('comm', coerce=int,
                       validators=[Required()])