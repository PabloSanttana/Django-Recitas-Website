from django.urls import path

from authors import views

app_name = "authors"

urlpatterns = [
    path('register/', views.authors_register, name='register'),
    path('register/create/', views.register_create, name='register_create'),

    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),

    path('logout/', views.logout_view, name='logout'),
    path('logout/user/', views.logout_user, name='logout_user'),

    path('dashboard/profile', views.profile_view, name='profile'),

    path('dashboard/create', views.create_recipe, name='create_recipe'),
]
