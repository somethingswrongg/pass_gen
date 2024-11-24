
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
    """функция входа пользователя на сайт"""

    if request.method == "GET":
        if request.user.is_authenticated:  # проеврка, выполнен ли вход пользователем
            return redirect('generator:home')  # если вход выполнен, то переадресация на страницу home.html

        return render(request, 'generator/login.html')  # если вход не выполнен, то переадресация на страницн login.html

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is not None:
        # при входе на страницу login.html выполняется проверка авторизации
        # если вход выполнен, то выполняется переадресация на страницу home.html
        login(request, user)
        return redirect('home')

    return render(request, "generator/login.html")


def logout_view(request: HttpRequest):
    """функция выхода пользователя из системы"""

    logout(request)
    return redirect(reverse('generator:home'))


def password(request):
    """функция генерации пароля в шаблоне home.html"""

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

    if request.user.is_authenticated:
        # если выполнен вход, то имя пользователя, сгенерированный пароль и когда создан пароль добавятся в бд
        user_instance = request.user
        password_to_models = Passwords(user=user_instance, password=thepassword, created_at=datetime)
        password_to_models.save()
    return render(request, 'generator/password.html', {'password': thepassword})


def home(request):
    return render(request, 'generator/home.html')


def about(request):
    return render(request, 'generator/about.html')


def pass_list(request):
    """функиця генерирует список созданных паролей пользователем, выполнившим вход на сайт"""

    context = {
        "passwords_list": Passwords.objects.filter(user=request.user),
    }
    return render(request, 'generator/created_pass.html', context=context)


class AboutMeView(TemplateView):
    template_name = "generator/about_me.html"


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # После успешной регистрации автоматически входим в систему
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # Перенаправляем на главную страницу или другую страницу
            return redirect('home')  # Замените 'home' на URL вашей главной страницы
    else:
        form = UserCreationForm()
    return render(request, 'generator/test-page.html', {'form': form})
