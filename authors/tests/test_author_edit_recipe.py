from django.urls import reverse
from recipes.tests.test_recipe_base import RecipeTestBase
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class AuthorDeleteRecipe(RecipeTestBase):

    def test_author_recipe_edit_get_id_not_found(self):
        self.make_author()
        self.client.login(
            username='RafaelaSantana',
            password='RafaelaSantana1234',
        )
        url = reverse('authors:recipe_edit', kwargs={'id': 1})
        response = self.client.get(url, follow=True)
        self.assertEqual(404, response.status_code)

    def test_author_edit_recipe_get_data_is_correct(self):
        self.make_recipe(is_published=False)
        self.client.login(
            username='RafaelaSantana',
            password='RafaelaSantana1234',
        )
        url = reverse('authors:recipe_edit', kwargs={'id': 1})
        response = self.client.get(url, follow=True)
        self.assertIn("Receita da Rafaela",
                      response.content.decode('utf-8'))

    def test_author_edit_recipe_success(self):
        self.make_recipe(is_published=False)
        self.client.login(
            username='RafaelaSantana',
            password='RafaelaSantana1234',
        )
        url = reverse('authors:recipe_edit', kwargs={'id': 1})
        response = self.client.get(url, follow=True)
        # Create a new image using PIL
        im = Image.new(mode='RGB', size=(200, 200))
        im_io = BytesIO()  # a BytesIO object for saving image
        im.save(im_io, 'JPEG')  # save the image to im_io
        im_io.seek(0)  # seek to the beginning

        image = InMemoryUploadedFile(
            im_io, None, 'random-name.jpg', 'image/jpeg', len(
                im_io.getvalue()) * 1024 * 1024, None
        )
        form_data = {
            'title': 'Recipe Title',
            'description': 'Description Recipe',
            'preparation_time': '2',
            'preparation_time_unit': 'Minutos',
            'servings': '2',
            'servings_unit': 'Pessoas',
            'preparation_steps': 'Preparation steps Preparation steps',
            'cover': image,
            'category': '1',
        }
        response = self.client.post(url, data=form_data, follow=True)
        self.assertIn("Edit with success.",
                      response.content.decode('utf-8'))
