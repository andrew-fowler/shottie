import requests


class SauceClient:
    platform_json = ""

    # Example platforms/webdriver response:
    #       {'short_version': '15', 'long_name': 'Microsoft Edge',
    #       'api_name': 'microsoftedge', 'long_version': '15.15063.',
    #       'latest_stable_version': '', 'automation_backend': 'webdriver', 'os': 'Windows 10'}


    @staticmethod
    def get_platforms():
        if SauceClient.platform_json == "":
            url = "https://saucelabs.com/rest/v1/info/platforms/webdriver"
            SauceClient.platform_json = requests.get(url).json()
            print(SauceClient.platform_json)
        return SauceClient.platform_json
