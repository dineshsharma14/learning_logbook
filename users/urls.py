"""Define URL patterns for users"""

from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    #Login Page
    path('login/',
         auth_views.LoginView.as_view(template_name= 'users/login.html'),
         name = "login"),

    #Logout Page
    path('logout',
         auth_views.LogoutView.as_view(template_name= 'users/login.html'),
         name = 'logout'),

    #Registeration page
    path('register', views.register, name = 'register'),
    ]
