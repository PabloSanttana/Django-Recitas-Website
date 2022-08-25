from unittest import TestCase
from recipes.forms import RecipeForm
from parameterized import parameterized
from django.test import TestCase as djangoTestCase
from django.urls import reverse
from recipes.models import Category
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class AuthorCreateRecipeFormUnitTest(TestCase):
    @parameterized.expand([
        ('title', 'Recipe Title'),
        ('description', 'Description recipe'),
        ('preparation_steps', 'How to prepare a  recipe'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RecipeForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('cover', 'Maximum size file ( 2MB ).')
    ])
    def test_fields_help_text(self, field, needed):
        form = RecipeForm()
        current = form[field].field.help_text
        self.assertEqual(needed, current)

    @parameterized.expand([
        ('title', 'Title'),
        ('description', 'Description'),
        ('preparation_time', 'Preparation time'),
        ('preparation_time_unit', 'Preparation time unit'),
        ('servings', 'Servings'),
        ('servings_unit', 'Servings unit'),
        ('preparation_steps', 'Preparation steps'),
        ('cover', 'Cover'),
        ('category', 'Category'),

    ])
    def test_fields_label(self, field, label):
        form = RecipeForm()
        current = form[field].field.label
        self.assertEqual(label, current)

# simulando um cadastro


class AuthorCreateRecipeIntegrationTest(djangoTestCase):
    def setUp(self, *args, **kwargs):
        form_data = {
            'username': 'RafaelaSantana',
            'first_name': 'Rafaela',
            'last_name': 'Santana',
            'email': 'Rafaela@gmail.com',
            'password': 'Abc123456789abc123',
            'password2': 'Abc123456789abc123'
        }
        url = reverse('authors:register_create')
        self.client.post(url, data=form_data, follow=True)
        # Create a new image using PIL
        im = Image.new(mode='RGB', size=(200, 200))
        im_io = BytesIO()  # a BytesIO object for saving image
        im.save(im_io, 'JPEG')  # save the image to im_io
        im_io.seek(0)  # seek to the beginning

        image = InMemoryUploadedFile(
            im_io, None, 'random-name.jpg', 'image/jpeg', len(
                im_io.getvalue()) * 1024 * 1024, None
        )
        self.form_data = {
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
        Category.objects.create(title='Carnes')
        return super().setUp(*args, **kwargs)

    def login_user_default(self):
        url = reverse('authors:login_create')
        form_data = {
            'username': 'RafaelaSantana',
            'password': 'Abc123456789abc123',
        }
        return self.client.post(url, data=form_data, follow=True)

    @parameterized.expand([
        ('title', 'This field is required'),
        ('description', 'This field is required'),
        ('preparation_time', 'This field is required'),
        ('preparation_time_unit', 'This field is required'),
        ('servings', 'This field is required'),
        ('servings_unit', 'This field is required'),
        ('preparation_steps', 'This field is required'),
        ('cover', 'This field is required'),
        ('category', 'This field is required'),

    ])
    def test_fields_cannot_be_empty(self, field, message):
        self.login_user_default()
        self.form_data[field] = ''
        url = reverse('authors:create_recipe')
        response = self.client.post(
            url, data=self.form_data, follow=True)
        self.assertIn(message, response.content.decode('utf-8'))
        self.assertIn(message, response.context['form'].errors.get(field))

    @parameterized.expand([
        ('title', 'abc', 'Make sure the value is at least 4 characters'),
        ('description', 'abc', 'Make sure the value is at least 4 characters'),
        ('preparation_time', '-1', 'Invalid number'),
        ('servings', '-1', 'Invalid number'),
    ])
    def test_fields_number_Invalid_and_min_length(self, field, value, message):
        self.login_user_default()
        url = reverse('authors:create_recipe')
        self.form_data[field] = value
        response = self.client.post(
            url, data=self.form_data, follow=True)
        self.assertIn(message, response.content.decode('utf-8'))
        self.assertIn(message, response.context['form'].errors.get(field))

    @parameterized.expand([
        ('title', 'Make sure the value is a maximum of 150 characters.',),
        ('description', 'Make sure the value is a maximum of 150 characters.'),
    ])
    def test_fields_max_length(self, field, message):
        self.login_user_default()
        url = reverse('authors:create_recipe')
        self.form_data[field] = "a"*151
        response = self.client.post(
            url, data=self.form_data, follow=True)
        self.assertIn(message, response.content.decode('utf-8'))
        self.assertIn(message, response.context['form'].errors.get(field))

    def test_create_successful(self):
        self.login_user_default()
        url = reverse('authors:create_recipe')
        response = self.client.post(
            url, data=self.form_data, follow=True)
        self.assertIn('Recipe create success.',
                      response.content.decode('utf-8'))
