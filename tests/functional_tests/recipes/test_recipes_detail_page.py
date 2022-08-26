from .base import RecipeBaseFunctionTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest


@pytest.mark.functional_test
class RecipeHomeFunctionTestCase(RecipeBaseFunctionTestCase):
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()
        title_needed = "Nova Receita de Carnes"
        recipes[len(recipes)-1].title = title_needed
        recipes[len(recipes)-1].save()
        # Usuário abre a página
        self.browser.get(self.live_server_url)
        recipe = self.browser.find_element(
            By.XPATH, '/html/body/div/div[2]/div[1]/div/div[1]/a')

        recipe.click()
        title = self.browser.find_element(
            By.CLASS_NAME, 'card-title')
        self.assertEqual(title_needed, title.text)
