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
