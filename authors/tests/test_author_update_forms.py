from unittest import TestCase
from authors.forms import UpdateAuthorForm
from parameterized import parameterized
from django.urls import reverse
from django.test import TestCase as djangoTestCase


class AuthorUpdateUnittest(TestCase):
    @parameterized.expand([
        ('username', 'Type your username'),
        ('first_name', 'Ex.: john'),
        ('last_name', 'Ex.: Doe'),
        ('email', 'Ex.: email@example.com'),

    ])
    def test_fields_placeholder(self, field, placeholder):
        form = UpdateAuthorForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
    ])
    def test_fields_is_correct_label(self, field, label):
        form = UpdateAuthorForm()
        current_label = form[field].field.label
        self.assertEqual(label, current_label)


class AuthorUpdateFromIntegrationTest(djangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'RafaelaSantana',
            'first_name': 'Rafaela',
            'last_name': 'Santana',
            'email': 'Rafaela@gmail.com',
            'password': 'Abc123456789abc123',
            'password2': 'Abc123456789abc123'
        }
        url = reverse('authors:register_create')
        self.client.post(url, data=self.form_data, follow=True)

        return super().setUp(*args, **kwargs)

    def login_user_default(self, username, password):
        url = reverse('authors:login_create')
        form_data = {
            'username': username,
            'password': password
        }
        return self.client.post(url, data=form_data, follow=True)

    def test_update_user_load_is_correct(self):
        self.login_user_default(
            username=self.form_data.get('username'),
            password=self.form_data.get('password')
        )
        url = reverse('authors:profile')
        response = self.client.get(url, follow=True)
        response.context['form'].initial['username']
        response.context['form'].initial['first_name']
        response.context['form'].initial['last_name']
        response.context['form'].initial['email']

        self.assertEqual(self.form_data.get('username'),
                         response.context['form'].initial['username'])
        self.assertEqual(self.form_data.get('first_name'),
                         response.context['form'].initial['first_name'])
        self.assertEqual(self.form_data.get('last_name'),
                         response.context['form'].initial['last_name'])
        self.assertEqual(self.form_data.get('email'),
                         response.context['form'].initial['email'])

    def test_update_username_and_email_is_already(self):
        form_data = {
            'username': 'Rafinha',
            'first_name': 'Rafinha',
            'last_name': 'Santana',
            'email': 'Rafinha@gmail.com',
            'password': 'Abc123456789abc123',
            'password2': 'Abc123456789abc123'
        }
        url = reverse('authors:register_create')
        self.client.post(url, data=form_data, follow=True)

        self.login_user_default(
            username=self.form_data.get('username'),
            password=self.form_data.get('password')
        )
        url = reverse('authors:profile')

        self.form_data.update(username='Rafinha')
        self.form_data.update(email='Rafinha@gmail.com')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn("Um usuário com este nome de usuário já existe.",
                      response.content.decode('utf-8'))
        self.assertIn(f'The email: Rafinha@gmail.com is already in use',
                      response.content.decode('utf-8'))
        self.assertIn("Um usuário com este nome de usuário já existe.",
                      response.context['form'].errors.get('username'))
        self.assertIn('The email: Rafinha@gmail.com is already in use',
                      response.context['form'].errors.get('email'))

    def test_update_is_correct(self):
        self.login_user_default(
            username=self.form_data.get('username'),
            password=self.form_data.get('password')
        )
        url = reverse('authors:profile')

        self.form_data["username"] = 'Rafinha'
        self.form_data["email"] = 'Rafaela@gmail.com'

        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertEqual(self.form_data.get('username'),
                         response.context['form'].initial['username'])
        self.assertEqual(self.form_data.get('email'),
                         response.context['form'].initial['email'])
        self.assertIn('Edit with success.',
                      response.content.decode('utf-8'))
