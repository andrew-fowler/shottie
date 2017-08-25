import requests


class SauceClient:
    platform_json = ""

    @staticmethod
    def get_platforms():
        if SauceClient.platform_json == "":
            url = "https://saucelabs.com/rest/v1/info/platforms/webdriver"
            SauceClient.platform_json = requests.get(url).json()
            print(SauceClient.platform_json)
        return SauceClient.platform_json

    @staticmethod
    def get_os_list():
        os_list = []
        for platform in SauceClient.get_platforms():
            if (platform['os'], platform['os']) not in os_list:
                os_list.append((platform['os'], platform['os']))

        os_list.sort(key=lambda tup: tup[1])
        return os_list

    @staticmethod
    def get_browser_list():
        browser_list = []
        for platform in SauceClient.get_platforms():
            if (platform['api_name'], platform['long_name']) not in browser_list:
                browser_list.append((platform['api_name'], platform['long_name']))

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
        return True