
from django.contrib import admin
from django.urls import path
from . import views
 
urlpatterns = [
    path("", views.Home,name="Home"),
    path("SignUp",views.SignUp,name="SignUp"),
    path("login",views.login_page,name="login"),
    path("logout",views.logout_page,name="logout"),
    path("ContentLol",views.ContentLol,name="ContentLol"),

 

  
]