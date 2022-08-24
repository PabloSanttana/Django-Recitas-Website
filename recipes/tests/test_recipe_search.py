from django.urls import reverse, resolve

from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch  # manipular variaveis de ambiente para os teste


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_function_is_correct(self):
        url = reverse('recipes:search')
        view = resolve(url)
        self.assertIs(view.func, views.recipe_search)

    def test_recipe_search_view_returns_stats_200_ok(self):
        url = reverse('recipes:search') + '?search=Receita'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_search_view_returns_stats_404_ok(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_template_is_corrent(self):
        url = reverse('recipes:search') + '?search=Receita'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/recipes_search.html')

    def test_recipe_search_template_no_recipes(self):
        url = reverse('recipes:search') + '?search=Receita'
        response = self.client.get(url)
        self.assertIn("Nenhuma receita encontrada",
                      response.content.decode('utf-8'))

    def test_recipe_search_template_loads_recipes(self):
        # criando uma recita
        r = self.make_recipe()
        url = reverse('recipes:search') + f'?search={r.title}'
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        recipes = response.context['recipes']
        self.assertIn(r.title, content)
        self.assertIn(r.author.first_name, content)
        self.assertIn('Carnes', content)
        self.assertEqual(len(recipes), 1)

    def test_recipe_search_template_dont_loads_recipes_not_published(self):
        """Test recipes is_published False not Show"""
        r = self.make_recipe(is_published=False)
        url = reverse('recipes:search') + f'?search={r.title}'
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        recipes = response.context['recipes']
        self.assertIn("Nenhuma receita encontrada", content)
        self.assertEqual(len(recipes), 0)

    @patch('recipes.views.PER_PAGE', new=9)
    def test_recipe_search_template_shows_recipes_is_pagination(self):
        r = self.make_recipe_in_batch()
        url = reverse('recipes:search') + f'?search={r[0].description}'
        response = self.client.get(url)
        recipes = response.context['recipes']
        paginator = recipes.paginator
        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 9)
        self.assertEqual(len(paginator.get_page(2)), 9)
        self.assertEqual(len(paginator.get_page(3)), 2)
