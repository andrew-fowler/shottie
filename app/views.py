from flask import render_template
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
    platforms = SauceAPI.get_platforms()

    os_list = []
    for platform in platforms:
        if not (platform['os'], platform['os']) in os_list:
            os_list.append((platform['os'], platform['os']))

    os_list.sort(key=lambda tup: tup[1])
    form.select_platform.choices = os_list

    # NOTE: This is example code
    #   - the browser select should be populated based on the OS choice
    #   - the browser select should be disabled by default
    browser_list = []
    for platform in platforms:
        if not (platform['long_name'], platform['long_name']) in browser_list:
            browser_list.append((platform['long_name'], platform['long_name']))

    browser_list.sort(key=lambda tup: tup[1])
    form.select_browser.choices = browser_list

    version_list = []
    for platform in platforms:
        if not (platform['short_version'], platform['short_version']) in version_list:
            version_list.append((platform['short_version'], platform['short_version']))

    version_list.sort(key=lambda tup: tup[1])
    form.select_version.choices = version_list

    if form.validate_on_submit():
        session['username'] = str(form.username.data)
        session['accesskey'] = str(form.accesskey.data)
        session['tunnelname'] = str(form.tunnelname.data)
        session['urls'] = str(form.urls.data)
        session['browser'] = str(form.browser.data)
        session['platform'] = str(form.platform.data)
        session['version'] = str(form.version.data)
        session['device'] = str(form.device.data)

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
    device = session['device']

    urls = str(urls).split(',')
    screenshots = []
    for url in urls:
        driver = ScreenShotTaker.get_sauce_labs_driver(username=username, accesskey=accesskey,
                                                       tunnelname=tunnelname,
                                                       browser=browser, platform=platform, version=version,
                                                       device=device)
        if driver:
            driver.get(url)
            screenshots.append(driver.get_screenshot_as_base64())
            driver.quit()

    return render_template('screenshots.html', title='screenshots',
                           url=urls,
                           browser=browser,
                           screenshots=screenshots)
