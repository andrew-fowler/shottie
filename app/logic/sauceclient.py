import requests


class SauceClient:
    platform_json = ""

    @staticmethod
    def get_platforms():
        if SauceClient.platform_json == "":
            url = "https://saucelabs.com/rest/v1/info/platforms/webdriver"
            SauceClient.platform_json = requests.get(url).json()
        return SauceClient.platform_json

    @staticmethod
    def get_os_list():
        os_list = []
        for platform in SauceClient.get_platforms():

            os = platform['os']

            if (os, os) not in os_list:
                os_list.append((os, os))

        os_list.sort(key=lambda tup: tup[1])
        return os_list

    @staticmethod
    def get_browser_list():
        browser_list = []
        for platform in SauceClient.get_platforms():

            short_browser_name = platform['api_name']
            long_browser_name = platform['long_name']

            if (short_browser_name, long_browser_name) not in browser_list:
                browser_list.append((short_browser_name, long_browser_name))

        browser_list.sort(key=lambda tup: tup[1])
        return browser_list

    @staticmethod
    def get_version_list():
        version_list = []
        for platform in SauceClient.get_platforms():

            version = platform['short_version']

            if (version, version) not in version_list:
                version_list.append((version, version))

        version_list.sort(key=lambda tup: tup[1], reverse=True)
        return version_list

    @staticmethod
    def is_combination_supported(os, browser, version):
        if os == "Linux" and browser == "Google Chrome":
            return False
        if version == "dev" or version == "beta":
            return False
        if (browser == "Google Chrome" or browser == "Firefox") and float(version) < 10:
            return False
        return True
