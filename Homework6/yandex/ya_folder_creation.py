import requests
import configparser


class YandexDisk:
    """
    Class to work with Yandex Disk API

    attributes:
    token: access token

    methods:
    create_folder: creates new folder
    """

    def __init__(self, token: str):
        self.token = token

    def create_folder(self, folder_name: str) -> int:
        """
        Sends put request to YD API to create new folder
        :param folder_name: name of new folder
        :return: response code
        """

        URL = 'https://cloud-api.yandex.net:443/v1/disk/resources'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
        params = {"path": folder_name}
        response = requests.put(URL, headers=headers, params=params)
        return response.status_code


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')
    user_token = config['YA']['token']

    ya = YandexDisk(user_token)

    ya.create_folder('Test_folder_pytest')
