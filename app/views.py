from flask import render_template, jsonify
from flask import session
from werkzeug.utils import redirect

from app import app
from app.forms import SessionForm
from app.logic.sauceapi import SauceAPI
from app.logic.shotter import ScreenShotTaker


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SessionForm()

    form.select_browser.choices = get_browser_list()
    form.select_platform.choices = get_os_list()
    form.select_version.choices = get_version_list()
    # form.select_browser.choices = [{None:None},{None:None}]
    # form.select_platform.choices = [{form.select_platform.data: form.select_platform.data}]
    # form.select_version.choices = [{form.select_version.data: form.select_version.data}]

    if form.validate_on_submit():
        session['username'] = str(form.username.data)
        session['accesskey'] = str(form.accesskey.data)
        session['tunnelname'] = str(form.tunnelname.data)
        session['urls'] = str(form.urls.data)
        # session['browser'] = str(form.browser.data)
        session['browser'] = str(form.select_browser.data)
        # session['platform'] = str(form.platform.data)
        session['platform'] = str(form.select_platform.data)
        # session['version'] = str(form.version.data)
        session['version'] = str(form.select_version.data)
        # session['device'] = str(form.device.data)

        return redirect('/screenshot')

    return render_template('index.html', title='Home', form=form)


@app.route('/screenshot', methods=['GET', 'POST'])
def take_screenshot():
    username = session['username']
    accesskey = session['accesskey']
    tunnelname = session['tunnelname']
    urls = session['urls']
    browser = session['browser']
    platform = session['platform']
    version = session['version']
    # device = session['device']

    urls = str(urls).split(',')
    screenshots = []
    for url in urls:
        screenshots.append(
            ScreenShotTaker.take_screenshot(username, accesskey, tunnelname, browser, platform, version, url))

    return render_template('screenshots.html', title='screenshots',
                           url=urls,
                           browser=browser,
                           screenshots=screenshots)


@app.route('/_get_browser_list/')
def _get_browser_list():
    browser_list = []
    for platform in SauceAPI.get_platforms():
        if not (platform['api_name'], platform['long_name']) in browser_list:
            browser_list.append((platform['api_name'], platform['long_name']))

    browser_list.sort(key=lambda tup: tup[1])

    return jsonify(browser_list)


@app.route('/_get_version_list/<browser>')
def _get_version_list(browser):
    version_list = []
    for platform in SauceAPI.get_platforms():
        if platform['api_name'] == browser and not (
                platform['short_version'], platform['short_version']) in version_list:
            version_list.append((platform['short_version'], platform['short_version']))

    version_list.sort(key=lambda tup: tup[1])

    return jsonify(version_list)


@app.route('/_get_os_list/<browser>')
def _get_os_list(browser):
    os_list = []
    for platform in SauceAPI.get_platforms():
        if platform['api_name'] == browser and not (platform['os'], platform['os']) in os_list:
            os_list.append((platform['os'], platform['os']))

    os_list.sort(key=lambda tup: tup[1])

    return jsonify(os_list)


def get_os_list():
    os_list = []
    for platform in SauceAPI.get_platforms():
        if not (platform['os'], platform['os']) in os_list:
            os_list.append((platform['os'], platform['os']))

    os_list.sort(key=lambda tup: tup[1])
    return os_list


def get_browser_list():
    browser_list = []
    for platform in SauceAPI.get_platforms():
        if not (platform['api_name'], platform['long_name']) in browser_list:
            browser_list.append((platform['api_name'], platform['long_name']))

    browser_list.sort(key=lambda tup: tup[1])
    return browser_list


def get_version_list():
    version_list = []
    for platform in SauceAPI.get_platforms():
        if not (platform['short_version'], platform['short_version']) in version_list:
            version_list.append((platform['short_version'], platform['short_version']))

    version_list.sort(key=lambda tup: tup[1])
    return version_list

# @app.route('/_get_browser_list/<os>')
# def _get_browser_list(os):
#     browser_list = []
#     for platform in SauceAPI.get_platforms():
#         if platform['os'] == os and not (platform['long_name'], platform['long_name']) in browser_list:
#             browser_list.append((platform['long_name'], platform['long_name']))
# 
#     browser_list.sort(key=lambda tup: tup[1])
# 
#     return jsonify(browser_list)
# 
# 
# @app.route('/_get_version_list/<browser>')
# def _get_version_list(browser):
#     version_list = []
#     for platform in SauceAPI.get_platforms():
#         if platform['long_name'] == browser and not (platform['short_version'], platform['short_version']) in version_list:
#             version_list.append((platform['short_version'], platform['short_version']))
# 
#     version_list.sort(key=lambda tup: tup[1])
# 
#     return jsonify(version_list)
# 
# 
# def get_os_list():
#     os_list = []
#     for platform in SauceAPI.get_platforms():
#         if not (platform['os'], platform['os']) in os_list:
#             os_list.append((platform['os'], platform['os']))
# 
#     os_list.sort(key=lambda tup: tup[1])
#     return os_list
# 
# 
# def get_browser_list():
#     browser_list = []
#     for platform in SauceAPI.get_platforms():
#         if not (platform['long_name'], platform['long_name']) in browser_list:
#             browser_list.append((platform['long_name'], platform['long_name']))
# 
#     browser_list.sort(key=lambda tup: tup[1])
#     return browser_list
# 
# 
# def get_version_list():
#     version_list = []
#     for platform in SauceAPI.get_platforms():
#         if not (platform['short_version'], platform['short_version']) in version_list:
#             version_list.append((platform['short_version'], platform['short_version']))
# 
#     version_list.sort(key=lambda tup: tup[1])
#     return version_list
