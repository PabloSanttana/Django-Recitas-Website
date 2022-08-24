from django.urls import path

from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipe_home, name='home'),
    path('recipe/<slug:slug>/', views.recipe_detail, name='detail')
]
