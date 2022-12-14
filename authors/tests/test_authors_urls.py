from unittest import TestCase
from django.urls import reverse


class AuthorRegisterUrlsTest(TestCase):
    def test_authors_register_urls_is_correct(self):
        url = reverse('authors:register')
        self.assertEqual(url, '/authors/register/')

    def test_authors_register_create_urls_is_correct(self):
        url = reverse('authors:register_create')
        self.assertEqual(url, '/authors/register/create/')

    def test_authors_login_urls_is_correct(self):
        url = reverse('authors:login')
        self.assertEqual(url, '/authors/login/')

    def test_authors_login_create_urls_is_correct(self):
        url = reverse('authors:login_create')
        self.assertEqual(url, '/authors/login/create/')

    def test_authors_profile_urls_is_correct(self):
        url = reverse('authors:profile')
        self.assertEqual(url, '/authors/dashboard/profile')

    def test_authors_logout_urls_is_correct(self):
        url = reverse('authors:logout')
        self.assertEqual(url, '/authors/logout/')

    def test_authors_create_recipe_urls_is_correct(self):
        url = reverse('authors:create_recipe')
        self.assertEqual(url, '/authors/dashboard/create')

    def test_authors_edit_recipe_urls_is_correct(self):
        url = reverse('authors:recipe_edit', kwargs={'id': '105'})
        self.assertEqual(url, '/authors/dashboard/recipe/105/edit/')

    def test_authors_list_recipe_urls_is_correct(self):
        url = reverse('authors:dashboard')
        self.assertEqual(url, '/authors/dashboard/')
