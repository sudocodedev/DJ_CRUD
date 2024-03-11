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
    path('create-profile/',views.CreateUserProfile, name='create-profile'),
    path('update-profile/<int:profileid>/',views.EditUserProfile, name='update-profile'),
    path('like-post/<int:postid>/',views.likePost, name='like-post'),
    path('bookmark-post/<int:postid>/',views.bookMarkPost, name='bookmark-post'),
    path('post-status/<int:postid>/',views.statusCheck, name='post-status'),
    path('trending-posts/',views.top3Posts, name='top-3-posts'),
    path('view-profile/<int:profileid>/',views.UserProfileView, name='userprofile-view'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

