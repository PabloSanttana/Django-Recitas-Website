from urllib import response
from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_function_is_correct(self):
        url = reverse('recipes:home')
        view = resolve(url)
        self.assertIs(view.func, views.recipe_home)

    def test_recipe_home_view_returns_stats_200_ok(self):
        url = reverse('recipes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_template_is_corrent(self):
        url = reverse('recipes:home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/recipes_home.html')

    def test_recipe_home_template_no_recipes(self):
        url = reverse('recipes:home')
        response = self.client.get(url)
        self.assertIn("Nenhuma receita encontrada",
                      response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        # criando uma recita
        r = self.make_recipe()
        url = reverse('recipes:home')
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        recipes = response.context['recipes']
        self.assertIn(r.title, content)
        self.assertIn(r.author.first_name, content)
        self.assertIn('Carnes', content)
        self.assertEqual(len(recipes), 1)

    def test_recipe_home_template_dont_loads_recipes_not_published(self):
        """Test recipes is_published False not Show"""
        self.make_recipe(is_published=False)
        url = reverse('recipes:home')
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        recipes = response.context['recipes']
        self.assertIn("Nenhuma receita encontrada", content)
        self.assertEqual(len(recipes), 0)
