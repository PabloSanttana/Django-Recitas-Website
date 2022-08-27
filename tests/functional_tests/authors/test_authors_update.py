from time import sleep
from .base import AuthorBaseFunctionTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AuthorsUpadateFunctionTestCase(AuthorBaseFunctionTestCase):

    def form_user_login(self, form):
        self.get_by_name(form, "username").send_keys("rafaelaSantana")
        self.get_by_name(form, "password").send_keys("Ab123456789")
        form.submit()

    def test_form_update_is_sucess(self):
        self.create_user_defualt_is_valid()
        form = self.get_form(path="/html/body/div/div[3]/form")
        self.form_user_login(form)
        form = self.get_form(path="/html/body/div/div[3]/div/form")
        self.get_by_name(form, "username").send_keys(Keys.BACKSPACE * 20)
        self.get_by_name(form, "username").send_keys("Rafaela")
        self.get_by_name(form, "email").send_keys(Keys.BACKSPACE * 20)
        self.get_by_name(form, "email").send_keys("santana@gmail.com")
        form.submit()
        messages_success = self.browser.find_element(
            By.CLASS_NAME, "alert-success")
        self.assertEqual(messages_success.text, "Edit with success.")

    def test_update_email_username_is_already(self):
        self.create_user_defualt_is_valid()
        self.create_user_defualt_is_valid(
            username="santana", email="santana@gmail.com")
        form = self.get_form(path="/html/body/div/div[3]/form")
        self.form_user_login(form)
        form = self.get_form(path="/html/body/div/div[3]/div/form")
        self.get_by_name(form, "email").send_keys(Keys.BACKSPACE * 20)
        self.get_by_name(form, "email").send_keys("santana@gmail.com")
        self.get_by_name(form, "username").send_keys(Keys.BACKSPACE * 20)
        self.get_by_name(form, "username").send_keys("santana")
        form.submit()
        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn(
            "The email: santana@gmail.com is already in use", body.text)
        self.assertIn(
            "Um usuário com este nome de usuário já existe.", body.text)
        self.assertIn(
            "Há erros no formulário, corrija-os e envie novamente.", body.text)
