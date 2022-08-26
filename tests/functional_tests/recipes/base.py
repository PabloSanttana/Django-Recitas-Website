# Sobe o servidor sem arquivos staticos
from django.test import LiveServerTestCase

# Servidor completo
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from utils.browser import make_chrome_browser
from recipes.tests.test_recipe_base import RecipeMixin
import time


class RecipeBaseFunctionTestCase(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, s=2):
        time.sleep(s)
