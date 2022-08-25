from django.shortcuts import render, redirect
from authors.forms import AuthorRegisterForm, LoginForm, UpdateAuthorForm
from recipes.forms import RecipeForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.


def authors_register(request):
    author_register_form_data = request.session.get(
        'author_register_form_data', None)
    form = AuthorRegisterForm(author_register_form_data)
    return render(request, 'authors/pages/authors_register.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()
    POST = request.POST
    request.session['author_register_form_data'] = POST
    form = AuthorRegisterForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is create, please log in.')

        del(request.session['author_register_form_data'])
        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create'),
    })


def login_create(request):
    if not request.POST:
        raise Http404()
    form = LoginForm(request.POST)
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        if authenticated_user is not None:
            messages.success(request, 'Your are logged in.')
            login(request, authenticated_user)
            return redirect('authors:profile')
        else:
            messages.error(request, 'Invalid credentials.')

    else:
        messages.error(request, 'Error to validate form data.')

    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def profile_view(request):
    user = User.objects.get(username=request.user.username)
    form = UpdateAuthorForm(
        request.POST or None,
        instance=user
    )

    if form.is_valid():
        form.save()
        messages.success(request, 'Edit with success.')
        return redirect('authors:profile')

    return render(request, 'authors/pages/profile.html', context={
        'form': form,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):

    return render(request, 'authors/pages/logout.html')


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_user(request):
    if not request.POST:
        return redirect('authors:login')

    if request.POST.get('username') != request.user.username:
        return redirect('authors:login')

    logout(request)
    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def create_recipe(request):
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.save()
        messages.success(request, 'Recipe create success.')
        return redirect('authors:create_recipe')

    return render(request, 'authors/pages/create_recipe.html', {'form': form})
