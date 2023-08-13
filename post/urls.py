from django.urls import path
from . import views

urlpatterns = [
    path('posts/',views.postPage,name='post-page'),
    path('create-post/',views.createPost,name='create-post'),
    path('update-post/<int:postid>',views.updatePost,name='update-post'),
    path('delete-post/<int:postid>',views.deletePost,name='delete-post'),
    path('detailed-post/<int:postid>',views.detailedPost,name='detailed-post'),
]
