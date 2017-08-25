from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class SessionForm(Form):
    username = StringField('username', validators=[DataRequired()], default="LBG_PENSION_USER")
    accesskey = StringField('accesskey', validators=[DataRequired()], default='4f2a1885-a5cb-4bcd-9fed-f8895b75731d')
    tunnelname = StringField('tunnelname')
    urls = StringField('urls', validators=[DataRequired()], default='http://www.google.com, http://www.msn.com')

    select_platform = SelectField('select_platform', choices=[], id='select_platform', coerce=str)
    select_browser = SelectField('select_browser', choices=[], id='select_browser', coerce=str)
    select_version = SelectField('select_version', choices=[], id='select_version', coerce=str)

    add = SubmitField(label="Add Combination")
    clear = SubmitField(label="Clear Combinations")
    runtests = SubmitField(label="Run Tests")
