import os
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib import messages
from recipes.models import Recipe
from utils.pagnation import make_pagination

# Create your views here.

PER_PAGE = int(os.environ.get('PER_PAGE', 9))
QTY_LINK_PAGE = int(os.environ.get('QTY_LINK_PAGE', 4))


def recipe_home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGE, QTY_LINK_PAGE)

    return render(request, 'recipes/pages/recipes_home.html', {
        'recipes': page_obj,
        'pagination_range': pagination_range
    })


def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, is_published=True)

    return render(request, 'recipes/pages/recipes_detail.html', {
        'recipe': recipe,
        'is_detail_page': True

    })


def recipe_category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id'))

    page_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGE, QTY_LINK_PAGE)
    return render(request, 'recipes/pages/recipes_category.html', {
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'category_title': f'{recipes[0].category.title} - categoria'
    })
