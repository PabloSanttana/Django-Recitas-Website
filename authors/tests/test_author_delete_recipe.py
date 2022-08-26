from django.urls import reverse
from recipes.tests.test_recipe_base import RecipeTestBase


class AuthorDeleteRecipe(RecipeTestBase):

    def test_dashboard_delete_method_get_is_redirect_corret(self):
        self.make_author()
        self.client.login(
            username='RafaelaSantana',
            password='RafaelaSantana1234',
        )
        url = reverse('authors:recipe_delete')
        response = self.client.get(url, follow=True)
        self.assertIn("Dashboard (RafaelaSantana)",
                      response.content.decode('utf-8'))

    def test_dashboard_delete_id_invalid_status_404_ok(self):
        self.make_author()
        self.client.login(
            username='RafaelaSantana',
            password='RafaelaSantana1234',
        )
        form_data = {
            'id': '10'
        }
        url = reverse('authors:recipe_delete')
        response = self.client.post(url, data=form_data, follow=True)
        self.assertEqual(404, response.status_code)

    def test_dashboard_delete_ok(self):
        self.make_recipe(is_published=False)
        self.client.login(
            username='RafaelaSantana',
            password='RafaelaSantana1234',
        )
        form_data = {
            'id': '1'
        }
        url = reverse('authors:recipe_delete')
        response = self.client.post(url, data=form_data, follow=True)

        self.assertIn("Delete with success.",
                      response.content.decode('utf-8'))
