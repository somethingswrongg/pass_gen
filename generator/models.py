from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=12, blank=True)


class Passwords(models.Model):
    password = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)


class UsersPasswords(models.Model):
    name_template = models.ForeignKey(Profile, on_delete=models.CASCADE)
    password_template = models.ForeignKey(Passwords, on_delete=models.CASCADE)
