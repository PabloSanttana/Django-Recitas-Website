from unittest import TestCase
from django.urls import reverse


class RecipesUrlsTest(TestCase):
    def test_recipe_home_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipe_detail_is_correct(self):
        url = reverse('recipes:detail', kwargs={'slug': 'slug-teste'})
        self.assertEqual(url, '/recipe/slug-teste/')
