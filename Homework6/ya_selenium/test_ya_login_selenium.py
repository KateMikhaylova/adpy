import unittest
import configparser

from selenium import webdriver

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

        # если смотреть вручную через браузер, там после нажатия кнопки ввода пароля открывается страница Яндекс ID
        # self.assertIn("Яндекс ID", driver.title)
        # Но код падает с ошибкой AssertionError: 'Яндекс ID' not found in 'Авторизация'
        # Если вывести на печать то, что видит драйвер на следующей странице, там такая картина

        print(driver.title)  # Тут будет название "Авторизация"
        print(driver.current_url)  # Тут адрес страницы вида https://passport.yandex.ru/auth/challenge?track_id=....
        # или просто https://passport.yandex.ru/auth/welcome
        print(driver.page_source)  # А тут html код страницы, на которой уже как бы введен логин, пароль,
        # есть кнопки Войти и Войти по QR коду, но нажать первую опять же не получается, при обращении к ней по id
        # пишет, что она скрыта другим элементом, а по другим параметрам обратиться не дает

        driver.find_element('id', "passp:sign-in").click()
        # selenium.common.exceptions.ElementClickInterceptedException: Message: Element <button id="passp:sign-in" class="Button2 Button2_size_l Button2_view_action Button2_width_max Button2_type_submit" type="submit"> is not clickable at point (683,445) because another element <div class="passp-page-overlay passp-page-overlay_showed"> obscures it

        # driver.find_element('type', "submit").click()
        # selenium.common.exceptions.InvalidArgumentException: Message: unknown variant `type`, expected one of `css selector`, `link text`, `partial link text`, `tag name`, `xpath` at line 1 column 16
        # driver.find_element('data-t', "button:action:passp:sign-in").click()
        # selenium.common.exceptions.InvalidArgumentException: Message: unknown variant `data-t`, expected one of `css selector`, `link text`, `partial link text`, `tag name`, `xpath` at line 1 column 18
        # driver.find_element('class', "Button2 Button2_size_l Button2_view_action Button2_width_max Button2_type_submit").click()
        # selenium.common.exceptions.InvalidArgumentException: Message: unknown variant `class`, expected one of `css selector`, `link text`, `partial link text`, `tag name`, `xpath` at line 1 column 17

    def tearDown(self):
        """
        closes driver attribute
        :return:
        """
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
