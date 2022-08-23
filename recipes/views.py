from django.shortcuts import render

# Create your views here.


def recipe_home(request):

    return render(request, 'recipes/pages/recipes_home.html')
