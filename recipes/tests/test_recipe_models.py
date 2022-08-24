from .test_recipe_base import RecipeTestBase
from django.utils.text import slugify


class RecipeModelTest(RecipeTestBase):
    def test_recipe_Model_category_is___str___title(self):
        category = self.make_category()

        self.assertEqual(str(category), category.title, )

    def test_recipe_model_recipe_is___str___title(self):
        recipe = self.make_recipe()
        self.assertEqual(str(recipe), recipe.title, )

    def test_recipe_model_recipe_is_get_absolute_url(self):
        recipe = self.make_recipe()
        url = recipe.get_absolute_url()
        self.assertEqual(f'/recipe/{recipe.slug}/', url)

    def test_recipe_model_recipe_slug_is_None(self):
        recipe = self.make_recipe(slug=None)
        slug = slugify(recipe.title)
        self.assertIn(slug, recipe.slug)
        self.assertEqual(len(slug) + 7, len(recipe.slug))
