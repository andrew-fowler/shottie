from flask_wtf import Form
from wtforms import StringField, BooleanField, SelectField
from wtforms.validators import DataRequired

from app.logic.sauceapi import SauceAPI


class SessionForm(Form):
    username = StringField('username', validators=[DataRequired()], default="")
    accesskey = StringField('accesskey', validators=[DataRequired()], default='')
    tunnelname = StringField('tunnelname')
    urls = StringField('urls', validators=[DataRequired()], default='http://www.google.com, http://www.msn.com')
    # platform = StringField('platform', validators=[DataRequired()], default='Windows 10')
    # browser = StringField('browser', validators=[DataRequired()], default='firefox')
    # version = StringField('version', default='')
    # device = StringField('device', default='')

    select_platform = SelectField('select_platform', choices=[], id='select_platform', coerce=str)
    select_browser = SelectField('select_browser', choices=[], id='select_browser', coerce=str)
    select_version = SelectField('select_version', choices=[], id='select_version', coerce=str)

