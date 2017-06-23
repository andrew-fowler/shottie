from urllib.error import URLError
from selenium import webdriver

from app import app


def create_session():
    return ""


class ScreenShotTaker:
    timeout = 60

    @staticmethod
    def get_sauce_labs_driver(browser, platform, version, device, username, accesskey, tunnelname):
        """Gets a driver object that is used to control a session on Sauce Labs.

        Parameters
        ----------
        test_name : str
            The name to give to the test. This is displayed on Sauce Labs.
        browser : str
            The browser to test on.
        platform : str
            The platform to test on.
        version : str
            The version of the browser to test on.
        device : str
            The device to test on. Only necessary for Android and iOS.
        tunnelname : str
            (Optional) The name of the tunnel to use, if required
        accesskey : str
            The API access key for the specified user
        username : str
            The Saucelabs username used to authenticate
        """

        try:
            caps = dict()
            caps['browserName'] = browser
            caps['platform'] = platform
            # or 'OS X' in platform
            if 'Windows' in platform:
                caps['screen-resolution'] = '1280x1024'
            elif platform in ['Linux']:
                caps['screen-resolution'] = '1024x768'
            caps['version'] = version

            if device is not None:
                caps['device'] = device

            caps['name'] = "Saucelabs Screenshot Tool"
            caps['commandTimeout'] = ScreenShotTaker.timeout * 2
            caps['maxDuration'] = 210
            caps['idleTimeout'] = ScreenShotTaker.timeout
            caps['locationContextEnabled'] = False
            caps['username'] = username
            caps['accessKey'] = accesskey
            # caps['parent-tunnel'] = SAUCE_PARENT_ACCOUNT
            caps['tunnel-identifier'] = tunnelname
            caps['deviceScreenshot'] = True

            try:
                driver = webdriver.Remote(
                    desired_capabilities=caps,
                    command_executor='http://ondemand.saucelabs.com:80/wd/hub'
                )
            except URLError as e:
                app.logger.error('Error: {0}\nDetails: {1}\nCaps: {2}'.format(e.reason, e.__class__.__name__, caps))
                return None
            except Exception as e:
                app.logger.error('Error: {0}\nDetails: {1}\nCaps: {2}'.format(e.__cause__, e.__class__.__name__, caps))
                return None

            return driver
        except Exception as e:
            app.logger.error(
                "HTTPError raised while trying to connect to SauceLabs:\n {0} {1}".format(str(e), "SAUCELABS_HUB_URL"))
            app.logger.error("Exception raised while trying to initialise a driver for SauceLabs: " + str(e))
            raise