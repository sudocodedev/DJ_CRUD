from django.db import models
from django.contrib.auth.models import User


class post(models.Model):
    title=models.CharField(max_length=100)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
