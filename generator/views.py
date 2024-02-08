import random
from datetime import datetime

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView

from generator.models import Passwords


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'generator/register.html'
    success_url = reverse_lazy('generator:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")

        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('generator:home')

        return render(request, 'generator/login.html')

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is not None:
        login(request, user)
        return redirect('home')

    return render(request, "generator/login.html")


def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse('generator:home'))


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

    password_to_models = Passwords(password=thepassword, created_at=datetime)

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
