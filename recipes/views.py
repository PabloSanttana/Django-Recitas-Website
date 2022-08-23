from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from recipes.models import Recipe

# Create your views here.


def recipe_home(request):
    recites = Recipe.objects.filter(is_published=True).order_by('-id')

    return render(request, 'recipes/pages/recipes_home.html', {
        'recipes': recites
    })


def recipe_detail(request, slug):
    recipe = Recipe.objects.filter(slug=slug, is_published=True).first()

    if recipe is None:
        messages.error(request, 'Nenhuma receita encontrada.')
        return redirect('recipes:home')

    return render(request, 'recipes/pages/recipes_detail.html', {
        'recipe': recipe,
        'is_detail_page': True

    })
