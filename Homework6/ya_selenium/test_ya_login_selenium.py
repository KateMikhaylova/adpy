import unittest
import configparser

from selenium import webdriver
from time import sleep

config = configparser.ConfigParser()
config.read('settings.ini')
login = config['YA']['login']
password = config['YA']['password']


class TestYandexLogin(unittest.TestCase):
    """
    Class to test log in to yandex.ru

    attributes:
    driver: Firefox WebDriver object

    methods:
    setUp: creates driver attribute
    tearDown: closes driver attribute
    test_ya_login: test for log in to yandex.ru
    """

    def setUp(self):
        """
        creates driver attribute
        :return:
        """
        self.driver = webdriver.Firefox()

    def test_ya_login(self):
        """
        test for log in to yandex.ru
        :return:
        """
        driver = self.driver
        driver.get("https://passport.yandex.ru/auth/")

        self.assertIn("Авторизация", driver.title)

        elem = driver.find_element('name', "login")
        elem.send_keys(login)
        driver.find_element('id', "passp:sign-in").click()

        elem = driver.find_element('name', "passwd")
        elem.send_keys(password)
        driver.find_element('id', "passp:sign-in").click()

        sleep(10)
        self.assertIn("Яндекс ID", driver.title)

    def tearDown(self):
        """
        closes driver attribute
        :return:
        """
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
