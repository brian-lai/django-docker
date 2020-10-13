"""Base Test Case to provide tooling to work with Selenium."""
from random import random
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from time import sleep

from django.conf import settings
from django.test import LiveServerTestCase


class BaseSeleniumTestCase(LiveServerTestCase):
    """Test Case to provide helper functions and tooling for Selenium.
    """
    host = settings.DOMAIN_NAME

    def setUp(self):
        super(BaseSeleniumTestCase, self).setUpClass()
        settings.HOST_PORT = str(self.server_thread.port)
        self.setUpTestData()

    @classmethod
    def setUpClass(cls):
        super(BaseSeleniumTestCase, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(BaseSeleniumTestCase, cls).tearDownClass()

    @classmethod
    def setUpTestData(cls):
        """Override in each test case to provide test data.
        """
        pass

    @staticmethod
    def get_url(host, path=''):
        """Work around interaction between django_hosts and selenium webdriver.
        """
        if not host:
            host = 'www'
        return '{host}.{domain}:{port}/{path}'.format(
            host=host,
            domain=settings.DOMAIN_NAME,
            port=settings.HOST_PORT,
            path=path
        )

    @staticmethod
    def send_keys_with_random_delay(element, keys):
        """Provides key input to a provided element.
        """
        for k in keys:
            element.send_keys(k)
            sleep(random() * 0.5)
        sleep(0.5)

    def login(self, username='', password=''):
        """Go to login page, and sign in to gist with provided credentials.
        """
        login_url = self.get_url('accounts', 'login/')
        self.selenium.get(login_url)
        self.fill_in_login_form(username, password)

    def fill_in_login_form(self, username='', password=''):
        """Fills in and submits login form and submits it.

        Call this instead of login() when selenium driver attempts to access a page,
        and gets redirected to the login page.
        """
        self.assertEqual(self.selenium.title, 'Login - GenePeeks')
        username_input = self.selenium.find_element_by_id('id_email')
        username_input.send_keys(username)
        password_input = self.selenium.find_element_by_id('id_password')
        password_input.send_keys(password)
        self.selenium.find_element_by_xpath('//*[@id="login-button-container"]/button').click()

    def fill_out_select2(self, field_label, query_string=''):
        """Solution to fill out select2 dropdowns in selenium tests.

        Gains focus of the widget by clicking label, enters query string and selects the first option.
        """
        field_select_action = ActionChains(self.selenium) \
            .click(field_label) \
            .send_keys(Keys.RETURN) \
            .send_keys(query_string)
        return_key_action = ActionChains(self.selenium).send_keys(Keys.RETURN)
        field_select_action.perform()
        sleep(1)
        return_key_action.perform()

    def logout(self, username='', password=''):
        """Log out of gist.
        """
        self.selenium.get(self.get_url('accounts', 'logout/'))
