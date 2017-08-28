from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
import os


class SessionForm(Form):
    default_urls = "https://the-internet.herokuapp.com/"

    default_commands = "find_element_by_xpath('//a[@href=\"/login\"]').click()\n" +\
                       "find_element_by_xpath('//input[@id=\"username\"]').send_keys('tomsmith')\n" + \
                       "find_element_by_xpath('//input[@id=\"password\"]').send_keys('SuperSecretPassword!')\n" + \
                        "find_element_by_xpath('//button[@type=\"submit\"]').click()"

    default_sauce_username = os.getenv('SAUCE_USERNAME', "")
    default_sauce_access_key = os.getenv('SAUCE_ACCESS_KEY', "")

    username = StringField('username', validators=[DataRequired()], default=default_sauce_username)
    accesskey = StringField('accesskey', validators=[DataRequired()], default=default_sauce_access_key)
    tunnelname = StringField('tunnelname')
    urls = StringField('urls', validators=[DataRequired()], default=default_urls)
    commands = StringField('commands', widget=TextArea(), default=default_commands)

    select_platform = SelectField('select_platform', choices=[], id='select_platform', coerce=str)
    select_browser = SelectField('select_browser', choices=[], id='select_browser', coerce=str)
    select_version = SelectField('select_version', choices=[], id='select_version', coerce=str)

    add = SubmitField(label="Add Combination")
    clear = SubmitField(label="Clear Combinations")
    runtests = SubmitField(label="Start Screenshotting")
