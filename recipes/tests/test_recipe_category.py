from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch  # manipular variaveis de ambiente para os teste


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_function_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': '1'})
        view = resolve(url)
        self.assertIs(view.func, views.recipe_category)

    def test_recipe_category_view_returns_stats_404_ok(self):
        url = reverse('recipes:category', kwargs={'category_id': '1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_returns_stats_200_ok(self):
        self.make_recipe()
        url = reverse('recipes:category', kwargs={'category_id': '1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_category_template_is_corrent(self):
        self.make_recipe()
        url = reverse('recipes:category', kwargs={'category_id': '1'})
        response = self.client.get(url)
        self.assertTemplateUsed(
            response, 'recipes/pages/recipes_category.html')

    def test_recipe_Category_template_loads_recipes(self):
        # criando uma recita
        r = self.make_recipe()
        url = reverse('recipes:category', kwargs={'category_id': '1'})
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        recipes = response.context['recipes']
        self.assertIn(r.title, content)
        self.assertIn(r.author.first_name, content)
        self.assertIn('Carnes', content)
        self.assertEqual(len(recipes), 1)

    def test_recipe_category_template_dont_loads_recipes_not_published(self):
        """Test recipes is_published False not Show"""
        self.make_recipe(is_published=False)
        url = reverse('recipes:category', kwargs={'category_id': '1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
