from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Passwords(models.Model):
    created_password = models.ManyToManyField(Profile, related_name='passwords')
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=14)