from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#Adding a natural key to User model, so it can be serialized as ForeignKey
def natural_key(self):
    return self.username

#Monkey_Patching
User.add_to_class("natural_key",natural_key)

class post(models.Model):
    title=models.CharField(max_length=100)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    genre=models.CharField(max_length=150)
    ratings=models.DecimalField(max_digits=3,decimal_places=2)
    image=models.ImageField(upload_to='posts_images/',blank=True)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    date_modified=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title}--{self.author}"

    class Meta:
       ordering=["-date_modified","-date_posted"] 

class comments(models.Model):
    post=models.ForeignKey(post,on_delete=models.CASCADE,related_name="comments")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments",null=True)
    body=models.CharField(max_length=200,blank=False)
    comment_posted=models.DateTimeField(auto_now_add=True)

    def str_comment_posted(self):
        return self.comment_posted.strftime("%b %d %y, %H:%M")

    def __str__(self) -> str:
        return f"{self.user} --> {self.body[:11]}"

    class Meta:
        ordering=["-comment_posted",]


