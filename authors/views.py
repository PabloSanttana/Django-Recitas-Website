from django.shortcuts import render, redirect
from authors.forms import AuthorRegisterForm, LoginForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

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
            return redirect('authors:login')
        else:
            messages.error(request, 'Invalid credentials.')

    else:
        messages.error(request, 'Error to validate form data.')

    return redirect('authors:login')