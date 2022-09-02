import pytest

import configparser
import requests

from ya_folder_creation import YandexDisk


class TestFolderCreation:
    """
    Class to test folder creation method of YandexDisk class

    attributes:
    ya:          attribute to store YandexDisk object to call method

    methods:
    setup:                          creates ya attribute, deletes folder from disk if present
    teardown:                       deletes folder from dist if created during test
    test_folder_creation_response:  tests folder creation by response code check
    test_folder_actual_presence:    tests folder creation by actual check of its presence through get request
    test_existing_folder_creation:  tests folder creation if folder is already created
    test_wrong_token:               tests folder creation with wrong token
    """

    def setup(self):
        """
        creates ya attribute, deletes folder from disk if present
        :return:
        """
        config = configparser.ConfigParser()
        config.read('settings.ini')
        user_token = config['YA']['token']

        self.ya = YandexDisk(user_token)

        URL = 'https://cloud-api.yandex.net:443/v1/disk/resources'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.ya.token}'}
        params = {"path": 'Test_folder_pytest', 'permanently': 'true'}
        requests.delete(URL, headers=headers, params=params)

    def teardown(self):
        """
        deletes folder from dist if created during test
        :return:
        """
        URL = 'https://cloud-api.yandex.net:443/v1/disk/resources'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.ya.token}'}
        params = {"path": 'Test_folder_pytest', 'permanently': 'true'}
        requests.delete(URL, headers=headers, params=params)

    def test_folder_creation_response(self):
        """
        tests folder creation by response code check.
        :return:
        """
        result = self.ya.create_folder('Test_folder_pytest')
        assert result == 201

    def test_folder_actual_presence(self):
        """
        tests folder creation by actual check of its presence through get request
        :return:
        """
        self.ya.create_folder('Test_folder_pytest')

        URL = 'https://cloud-api.yandex.net:443/v1/disk/resources'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.ya.token}'}
        params = {"path": 'Test_folder_pytest'}
        response = requests.get(URL, headers=headers, params=params).json()
        assert 'error' not in response and response['type'] == 'dir'

    def test_existing_folder_creation(self):
        """
        tests folder creation if folder is already created
        :return:
        """
        self.ya.create_folder('Test_folder_pytest')
        result = self.ya.create_folder('Test_folder_pytest')
        assert result == 409

    def test_wrong_token(self):
        """
        tests folder creation with wrong token
        :return:
        """
        correct_token = self.ya.token
        self.ya.token = 'wrong_token'
        result = self.ya.create_folder('Test_folder_pytest')
        assert result == 401
        self.ya.token = correct_token
