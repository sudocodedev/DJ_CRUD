from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class post(models.Model):
    title=models.CharField(max_length=100)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    genre=models.CharField(max_length=150)
    ratings=models.DecimalField(max_digits=3,decimal_places=2)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    date_modified=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title}--{self.author}"

