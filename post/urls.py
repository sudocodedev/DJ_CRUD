from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('posts/',views.postPage,name='post-page'),
    path('create-post/',views.createPost,name='create-post'),
    path('update-post/<int:postid>',views.updatePost,name='update-post'),
    path('delete-post/<int:postid>',views.deletePost,name='delete-post'),
    path('detailed-post/<int:postid>',views.detailedPost,name='detailed-post'),
    path('comments/<str:postid>/',views.LoadComments,name='load-comments'),
    path('post-comment/<str:postid>/',views.PostComment,name='post-comment'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

