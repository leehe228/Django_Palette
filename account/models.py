from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(models.Model):
    userEmail = models.CharField(primary_key=True, max_length=200)
    userPassword = models.CharField(max_length=200)
    userName = models.CharField(max_length=100)
    userAge = models.IntegerField()
    userInterest = models.CharField(max_length=200)
    userLike = models.TextField(default='')
    userCreated = models.TextField(default='')
    userCode = models.CharField(max_length=20, default ='')
    userSex = models.CharField(null = True, default = '', max_length=10)
    userPaid = models.IntegerField(default=0)

    def __str__(self):
        return self.userEmail

# Create your models here.
