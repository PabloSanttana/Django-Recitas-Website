from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_function_is_correct(self):
        url = reverse('recipes:detail', kwargs={'slug': 'slug-teste'})
        view = resolve(url)
        self.assertIs(view.func, views.recipe_detail)

    def test_recipe_detail_view_returns_stats_404_ok(self):
        url = reverse('recipes:detail', kwargs={'slug': 'slug-teste'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_returns_stats_200_ok(self):
        recipe = self.make_recipe()
        url = reverse('recipes:detail', kwargs={'slug': recipe.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_template_is_corrent(self):
        recipe = self.make_recipe()
        url = reverse('recipes:detail', kwargs={'slug': recipe.slug})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/recipes_detail.html')

    def test_recipe_detail_template_loads_recipes(self):
        # criando uma recita
        recipe = self.make_recipe()
        url = reverse('recipes:detail', kwargs={'slug': recipe.slug})
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        self.assertIn(recipe.title, content)
        self.assertIn(recipe.author.first_name, content)
        self.assertIn('Carnes', content)

    def test_recipe_detail_template_dont_loads_recipes_not_published(self):
        """Test recipes is_published False not Show"""
        recipe = self.make_recipe(is_published=False)
        url = reverse('recipes:detail', kwargs={'slug': recipe.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
