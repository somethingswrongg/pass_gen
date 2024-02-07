import random
from audioop import reverse
from datetime import datetime

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from generator.models import Passwords, Profile


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'generator/register.html'
    success_url = reverse_lazy('generator:about-me')


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('generator:home')

        return render(request, 'generator/login.html')

    username = Profile.user
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')

    return render(request, "generator/login.html", {"error": "Invalid login credentials"})


def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse('home'))


def password(request):
    characters = list('qwertyuiopasdfghjklzxcvbnm')

    if request.GET.get('uppercase'):
        characters.extend(list('QWERTYUIOPASDFGHJKLZXCVBNM'))
    if request.GET.get('special'):
        characters.extend(list('!@#$%^&*()_+'))
    if request.GET.get('numbers'):
        characters.extend(list('0123456789'))

    lenght = int(request.GET.get('lenght', 12))
    thepassword = ''

    for x in range(lenght):
        thepassword += random.choice(characters)

    name = User.__name__

    password_to_models = Passwords(created_password=thepassword, created_at=datetime)
    password_to_models.save()

    return render(request, 'generator/password.html', {'password': thepassword})


def home(request):
    return render(request, 'generator/home.html')


def about(request):
    return render(request, 'generator/about.html')


def pass_list(request):
    context = {
        "passwords_list": Passwords.objects.all(),
    }

    return render(request, 'generator/created_pass.html', context=context)


class AboutMeView(TemplateView):
    template_name = "generator/about_me.html"
