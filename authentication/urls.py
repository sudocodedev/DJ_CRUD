from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginUser,name='login-page'),
    path('logout/',views.logoutUser,name='logout-page'),
    path('register/',views.registerUser,name='register-page'),
    path('activate/<uidb64>/<token>/',views.activate,name="activate"),
    path('reset-password/',views.resetPassword,name="reset-password"),
    path('reset/<uidb64>/<token>/',views.confirmResetPassword,name="reset-confirm"),
]