from flask import render_template, jsonify
from flask import session
from werkzeug.utils import redirect

from app import app
from app.forms import SessionForm
from app.logic.session_access import get_urls_from_session, get_combinations_from_session, get_tunnelname_from_session, \
    get_access_key_from_session, get_username_from_session
from app.logic.session_handler import clear_saved_combinations, add_new_combination, persist_run_inputs
from app.logic.sauceclient import SauceClient
from app.logic.shotter import ScreenShotTaker


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SessionForm()

    form.select_browser.choices = SauceClient.get_browser_list()
    form.select_platform.choices = SauceClient.get_os_list()
    form.select_version.choices = SauceClient.get_version_list()

    if form.validate_on_submit():
        if form.clear.data:
            clear_saved_combinations(session)
        elif form.add.data:
            add_new_combination(form, session)
            return render_template('index.html', title='Home', form=form,
                                   saved_combinations=session['saved_combinations'])

        elif form.runtests.data:
            persist_run_inputs(form, session)
            return redirect('/screenshot')
    else:
        clear_saved_combinations(session)

    return render_template('index.html', title='Home', form=form)


@app.route('/screenshot', methods=['GET', 'POST'])
def take_screenshot():
    username = get_username_from_session(session)
    accesskey = get_access_key_from_session(session)
    tunnelname = get_tunnelname_from_session(session)
    combinations = get_combinations_from_session(session)
    urls = get_urls_from_session(session)

    screenshots = []
    for url in urls:
        for combination in combinations:
            screenshots.append(
                ScreenShotTaker.take_screenshot(username, accesskey, tunnelname, combination['browser'],
                                                combination['platform'], combination['version'], url)
            )

    return render_template('screenshots.html', title='screenshots',
                           url=urls,
                           screenshots=screenshots)


@app.route('/browsers/', methods=['GET'])
def _get_browser_list():
    browser_list = []
    for platform in SauceClient.get_platforms():
        if not (platform['api_name'], platform['long_name']) in browser_list:
            browser_list.append((platform['api_name'], platform['long_name']))

    browser_list.sort(key=lambda tup: tup[1])

    return jsonify(browser_list)


@app.route('/versions/<browser>', methods=['GET'])
def _get_version_list(browser):
    version_list = []
    for platform in SauceClient.get_platforms():
        if platform['api_name'] == browser and not (
                platform['short_version'], platform['short_version']) in version_list:
            if SauceClient.is_combination_supported(os=platform['os'], browser=platform['long_name'],
                                                    version=platform['short_version']):
                version_list.append((platform['short_version'], platform['short_version']))

    version_list.sort(key=lambda tup: tup[1], reverse=True)

    return jsonify(version_list)


@app.route('/operating_systems/<browser>', methods=['GET'])
def _get_os_list(browser):
    os_list = []
    for platform in SauceClient.get_platforms():
        if platform['api_name'] == browser and not (platform['os'], platform['os']) in os_list:
            if SauceClient.is_combination_supported(os=platform['os'], browser=platform['long_name'], version=platform['short_version']):
                os_list.append((platform['os'], platform['os']))

    os_list.sort(key=lambda tup: tup[1])

    return jsonify(os_list)
