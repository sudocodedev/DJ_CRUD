from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginUser,name='login-page'),
    path('logout/',views.logoutUser,name='logout-page'),
    path('register/',views.registerUser,name='register-page'),
]