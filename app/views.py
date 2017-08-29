from threading import Thread

from flask import make_response
from flask import render_template, jsonify
from flask import request
from flask import session
from werkzeug.utils import redirect

from app import app
from app.forms import SessionForm
from app.logic.session_access import get_urls_from_session, get_combinations_from_session, get_tunnelname_from_session, \
    get_access_key_from_session, get_username_from_session, get_commands_from_session
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

    if request.cookies.get('default_sauce_access_key') is not None:
        form.default_sauce_access_key = request.cookies.get('default_sauce_access_key')

    if request.cookies.get('default_sauce_username') is not None:
        form.default_sauce_username = request.cookies.get('default_sauce_username')

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

    resp = make_response(render_template('index.html', title='Home', form=form))
    resp.set_cookie('default_sauce_access_key', str(form.accesskey.data))
    resp.set_cookie('default_sauce_username', str(form.username.data))
    return resp


@app.route('/screenshot', methods=['GET', 'POST'])
def take_screenshot():
    username = get_username_from_session(session)
    accesskey = get_access_key_from_session(session)
    tunnelname = get_tunnelname_from_session(session)
    combinations = get_combinations_from_session(session)
    urls = get_urls_from_session(session)
    commands = get_commands_from_session(session)

    screenshots = []
    threadpool = []

    for url in urls:
        for combination in combinations:
            threadpool.append(Thread(target=ScreenShotTaker.take_screenshot,
                                     kwargs={'username': username, 'accesskey': accesskey, 'tunnelname': tunnelname,
                                             'browser': combination['browser'], 'platform': combination['platform'],
                                             'version': combination['version'], 'url': url, 'commands': commands,
                                             'results': screenshots}))

    for thread in threadpool:
        thread.start()
    for thread in threadpool:
        thread.join()

    return render_template('screenshots.html', title='screenshots',
                           url=urls,
                           screenshots=screenshots)


@app.route('/browsers/', methods=['GET'])
def _get_browser_list():
    browser_list = SauceClient.get_browser_list()
    return jsonify(browser_list)


@app.route('/versions/<os>/<browser>', methods=['GET'])
def _get_version_list_for_os_and_browser(os, browser):
    version_list = SauceClient.get_versions_for_os_and_browser(os, browser)
    return jsonify(version_list)


@app.route('/operating_systems/<browser>', methods=['GET'])
def _get_os_list(browser):
    os_list = SauceClient.get_operating_systems_for_browser(browser)
    return jsonify(os_list)
