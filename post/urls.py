from django.urls import path
from . import views

urlpatterns = [
    path('posts/',views.postPage,name='post-page'),
    path('create/',views.createPost,name='create-post'),
]
