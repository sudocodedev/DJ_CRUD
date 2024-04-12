from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from tinymce.models import HTMLField

#Adding a natural key to User model, so it can be serialized as ForeignKey
def natural_key(self):
    return self.username

#Monkey_Patching
User.add_to_class("natural_key",natural_key)


class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name="profile_info")
    profileBackground=models.ImageField(upload_to='profile_images/',blank=True, default='profile_images/defaultBackground.jpg')
    profileImg=models.ImageField(upload_to='profile_images/', blank=True, default='profile_images/defaultUser.jpg')
    firstName=models.CharField(max_length=30, blank=False, null=False)
    lastName=models.CharField(max_length=30, blank=False, null=False)
    pronoun=models.CharField(max_length=15, blank=True, null=True)
    bio=HTMLField()
    location=models.CharField(max_length=50, blank=False, null=False) #state/ country
    doj=models.DateField(auto_now_add=True) #date of joining
    followers=models.ManyToManyField(User,related_name="following")
    instagram=models.URLField(max_length=150)
    x=models.URLField(max_length=150)
    github=models.URLField(max_length=150)
    telegram=models.URLField(max_length=150)

    def __str__(self) -> str:
        return self.firstName+" "+self.lastName

class GenreList(models.Model):
    name=models.CharField(max_length=40)
    slug=models.SlugField(max_length=50, blank=True)
    description=models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name

class post(models.Model):
    title=models.CharField(max_length=100)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    tags=models.ManyToManyField(GenreList)
    genre=models.CharField(max_length=150, null=True, blank=True)
    ratings=models.DecimalField(max_digits=3,decimal_places=2,null=True,blank=True)
    image=models.ImageField(upload_to='posts_images/',blank=True)
    content=HTMLField()
    date_posted=models.DateTimeField(default=timezone.now)
    date_modified=models.DateTimeField(auto_now=True)
    likes=models.ManyToManyField(User, related_name='liked_post')
    bookmark=models.ManyToManyField(User, related_name='bookmarked_post')
    isDraft=models.BooleanField(default=False)

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

    def profile_pic_link(self):
        return self.user.profile_info.profileImg.url

    def __str__(self) -> str:
        return f"{self.user} --> {self.body[:11]}"

    class Meta:
        ordering=["-comment_posted",]


