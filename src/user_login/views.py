from django.contrib.auth import login, authenticate, logout
from django.http import request  # add to imports
from django.shortcuts import render, redirect
from . import forms
from django.conf import settings
# from django.http import HttpResponse
# Create your views here.


def index(request):
   # return HttpResponse("<h1>Le Exemple</h1>")
    return render(request, "user_login/index.html")


def logout_user(request):
    logout(request)
    # return redirect('login.html')
    return login_page(request)


def login_page(request, msg=False):
    form = forms.LoginForm()
    message = msg
    if not message:
        message = ''

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
               # message = f'Bienvenue {user.username}!'
                return redirect("home")
            else:
                message = 'Vos identifiants sont incorrects'
    return render(
        request, 'authentication/login.html', context={'form': form, 'message': message})


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})
