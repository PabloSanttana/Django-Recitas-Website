from unittest import TestCase
from django.urls import reverse


class RecipesUrlsTest(TestCase):
    def test_recipe_home_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipe_detail_is_correct(self):
        url = reverse('recipes:detail', kwargs={'slug': 'slug-teste'})
        self.assertEqual(url, '/recipes/slug-teste/')

    def test_recipe_category_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': '1'})
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipe_search_is_correct(self):
        url = reverse('recipes:search',)
        self.assertEqual(url, '/recipes/search/')
