import requests


class SauceAPI:
    platform_json = ""

    @staticmethod
    def get_platforms():
        if SauceAPI.platform_json == "":
            url = "https://saucelabs.com/rest/v1/info/platforms/webdriver"
            SauceAPI.platform_json = requests.get(url).json()
            # Gives list of
            #       {'short_version': '15', 'long_name': 'Microsoft Edge',
            #       'api_name': 'microsoftedge', 'long_version': '15.15063.',
            #       'latest_stable_version': '', 'automation_backend': 'webdriver', 'os': 'Windows 10'}

        return SauceAPI.platform_json
