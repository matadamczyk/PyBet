from django.db import models

# Create your models here.

class Login(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)