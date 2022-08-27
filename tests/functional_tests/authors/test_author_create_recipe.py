from recipes.models import Category
from .base import AuthorBaseFunctionTestCase
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.parent.parent

IMGSMALL = 'frango.jpeg'
IMGFULL = "max2bm.jpeg"
IMGSMALL_PATH = ROOT_PATH / 'base_static'/'global' / 'file' / IMGSMALL
IMGFULL_PATH = ROOT_PATH / 'base_static'/'global' / 'file' / IMGFULL


class AuthorsCreateRecipeFunctionTestCase(AuthorBaseFunctionTestCase):
    def setUp(self, *args, **kwargs):
        User.objects.create_user(username='RafaelaSantana',
                                 email='Rafaela@gmail.com',
                                 password='Abc123456789abc123',
                                 first_name='Rafaela',
                                 last_name='Santana',
                                 )
        Category.objects.create(title='Carnes')
        return super().setUp(*args, **kwargs)

    def login_user_default(self):
        self.browser.get(self.live_server_url + '/authors/login/')
        form = self.get_form(path="/html/body/div/div[2]/form")
        self.get_by_name(form, "username").send_keys("RafaelaSantana")
        self.get_by_name(form, "password").send_keys("Abc123456789abc123")
        form.submit()

    def test_author_create_recipe_is_sucess(self):
        self.login_user_default()
        self.browser.get(self.live_server_url + '/authors/dashboard/create')
        form = self.get_form(path="/html/body/div/div[2]/div/form")
        self.get_by_name(form, "title").send_keys("This field is required")
        self.get_by_name(form, "description").send_keys(
            "This field is required")
        self.get_by_name(form, "preparation_time").send_keys("23")
        self.get_by_name(form, "servings").send_keys("3")
        self.get_by_name(form, "category").send_keys("Carnes")
        self.get_by_name(form, "preparation_steps").send_keys(
            "This field is required")
        self.get_by_name(form, "cover").send_keys(f'{IMGSMALL_PATH}')
        form.submit()
        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn("Recipe create success.",
                      body.text)

    def test_author_create_recipe_file_max_size(self):
        self.login_user_default()
        self.browser.get(self.live_server_url + '/authors/dashboard/create')
        form = self.get_form(path="/html/body/div/div[2]/div/form")
        self.get_by_name(form, "title").send_keys("This field is required")
        self.get_by_name(form, "description").send_keys(
            "This field is required")
        self.get_by_name(form, "preparation_time").send_keys("23")
        self.get_by_name(form, "servings").send_keys("3")
        self.get_by_name(form, "category").send_keys("Carnes")
        self.get_by_name(form, "preparation_steps").send_keys(
            "This field is required")
        self.get_by_name(form, "cover").send_keys(f'{IMGFULL_PATH}')
        form.submit()
        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn('Maximum size reached ( 2MB )', body.text)
        self.assertIn(
            'Há erros no formulário, corrija-os e envie novamente.', body.text)
