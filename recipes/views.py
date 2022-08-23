from django.shortcuts import render
from recipes.models import Recipe

# Create your views here.


def recipe_home(request):
    recites = Recipe.objects.filter(is_published=True).order_by('-id')

    return render(request, 'recipes/pages/recipes_home.html', {
        'recipes': recites
    })
