from django.urls import reverse
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from recipes.tests.test_recipe_base import RecipeTestBase

# simulando um cadastro


class AuthorDashboardIntegrationTest(RecipeTestBase):

    def test_dashboard_template_and_logged_in_is_correct(self):
        self.make_author()
        self.client.login(
            username='RafaelaSantana',
            password='RafaelaSantana1234',
        )
        url = reverse('authors:dashboard')
        response = self.client.get(url)
        self.assertIn("RafaelaSantana", response.content.decode('utf-8'))
        self.assertIn("Dashboard (RafaelaSantana)",
                      response.content.decode('utf-8'))

    def test_dashboard_authors_not_logged_in(self):
        self.make_author()
        url = reverse('authors:dashboard')
        response = self.client.get(url, follow=True)
        self.assertIn("Login", response.content.decode('utf-8'))
        self.assertNotIn("Dashboard (RafaelaSantana)",
                         response.content.decode('utf-8'))

    def test_dashboard_list_recipe_is_correct(self):
        recipe = self.make_recipe(is_published=False)
        url = reverse('authors:dashboard')
        self.client.login(
            username='RafaelaSantana',
            password='RafaelaSantana1234',
        )
        response = self.client.get(url, follow=True)
        self.assertIn(recipe.title, response.content.decode('utf-8'))
        self.assertIn(f'{recipe.id}', response.content.decode('utf-8'))
