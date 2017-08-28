from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class SessionForm(Form):
    default_urls = "http://www.google.com, http://www.msn.com"
    default_urls = "https://the-internet.herokuapp.com/"

    default_commands = "find_element_by_xpath('//body')"
    default_commands = "find_element_by_xpath('//a[@href=\"/login\"]').click()\nfind_element_by_xpath('//input[@id=\"username\"]').send_keys('Test')"

    username = StringField('username', validators=[DataRequired()], default="LBG_PENSION_USER")
    accesskey = StringField('accesskey', validators=[DataRequired()], default='4f2a1885-a5cb-4bcd-9fed-f8895b75731d')
    tunnelname = StringField('tunnelname')
    urls = StringField('urls', validators=[DataRequired()], default=default_urls)
    commands = StringField('commands', widget=TextArea(), default=default_commands)

    select_platform = SelectField('select_platform', choices=[], id='select_platform', coerce=str)
    select_browser = SelectField('select_browser', choices=[], id='select_browser', coerce=str)
    select_version = SelectField('select_version', choices=[], id='select_version', coerce=str)

    add = SubmitField(label="Add Combination")
    clear = SubmitField(label="Clear Combinations")
    runtests = SubmitField(label="Run Tests")
