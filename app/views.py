from flask import render_template, jsonify
from flask import session
from werkzeug.utils import redirect

from app import app
from app.forms import SessionForm
from app.logic.sauceclient import SauceClient
from app.logic.shotter import ScreenShotTaker


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SessionForm()

    form.select_browser.choices = get_browser_list()
    form.select_platform.choices = get_os_list()
    form.select_version.choices = get_version_list()

    if form.validate_on_submit():
        if form.clear.data:
            session['saved_combinations'] = list()
        elif form.add.data:
            record_to_add = {"browser": form.select_browser.data,
                             "platform": form.select_platform.data,
                             "version": form.select_version.data}

            if 'saved_combinations' in session:
                saved_combinations = session['saved_combinations']
                saved_combinations.append(record_to_add)
                session['saved_combinations'] = saved_combinations
            else:
                session['saved_combinations'] = [record_to_add]

            return render_template('index.html', title='Home', form=form,
                                   saved_combinations=session['saved_combinations'])

        elif form.runtests.data:
            session['username'] = str(form.username.data)
            session['accesskey'] = str(form.accesskey.data)
            session['tunnelname'] = str(form.tunnelname.data)
            session['urls'] = str(form.urls.data)

            return redirect('/screenshot')
    else:
        session['saved_combinations'] = list()

    return render_template('index.html', title='Home', form=form)


@app.route('/screenshot', methods=['GET', 'POST'])
def take_screenshot():
    username = session['username']
    accesskey = session['accesskey']
    tunnelname = session['tunnelname']
    urls = session['urls']
    combinations = session['saved_combinations']

    urls = str(urls).split(',')
    screenshots = []
    for url in urls:
        for combination in combinations:
            screenshots.append(
                ScreenShotTaker.take_screenshot(username, accesskey, tunnelname, combination['browser'],
                                                combination['platform'], combination['version'], url)
            )

    return render_template('screenshots.html', title='screenshots',
                           url=urls,
                           browser=combination['browser'],
                           screenshots=screenshots)


@app.route('/_get_browser_list/')
def _get_browser_list():
    browser_list = []
    for platform in SauceClient.get_platforms():
        if not (platform['api_name'], platform['long_name']) in browser_list:
            browser_list.append((platform['api_name'], platform['long_name']))

    browser_list.sort(key=lambda tup: tup[1])

    return jsonify(browser_list)


@app.route('/_get_version_list/<browser>')
def _get_version_list(browser):
    version_list = []
    for platform in SauceClient.get_platforms():
        if platform['api_name'] == browser and not (
                platform['short_version'], platform['short_version']) in version_list:
            version_list.append((platform['short_version'], platform['short_version']))

    version_list.sort(key=lambda tup: tup[1], reverse=True)

    return jsonify(version_list)


@app.route('/_get_os_list/<browser>')
def _get_os_list(browser):
    os_list = []
    for platform in SauceClient.get_platforms():
        if platform['api_name'] == browser and not (platform['os'], platform['os']) in os_list:
            if is_combination_supported(os=platform['os'], browser=platform['long_name']):
                os_list.append((platform['os'], platform['os']))

    os_list.sort(key=lambda tup: tup[1])

    return jsonify(os_list)


def get_os_list():
    os_list = []
    for platform in SauceClient.get_platforms():
        if (platform['os'], platform['os']) not in os_list:
            os_list.append((platform['os'], platform['os']))

    os_list.sort(key=lambda tup: tup[1])
    return os_list


def get_browser_list():
    browser_list = []
    for platform in SauceClient.get_platforms():
        if (platform['api_name'], platform['long_name']) not in browser_list:
            browser_list.append((platform['api_name'], platform['long_name']))

    browser_list.sort(key=lambda tup: tup[1])
    return browser_list


def get_version_list():
    version_list = []
    for platform in SauceClient.get_platforms():
        if (platform['short_version'], platform['short_version']) not in version_list:
            version_list.append((platform['short_version'], platform['short_version']))

    version_list.sort(key=lambda tup: tup[1], reverse=True)
    return version_list


def is_combination_supported(os, browser):
    if os == "Linux" and browser == "Google Chrome":
        return False
    return True
