from django.db import models
from django.contrib.auth.models import User

class ExtUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token_limit = models.IntegerField(default=4096)
    rate_limit = models.IntegerField(default=3)

class Message(models.Model):
    role = models.CharField(max_length=128)
    content = models.CharField(max_length=4096)
    user = models.ForeignKey(ExtUser, on_delete=models.CASCADE)