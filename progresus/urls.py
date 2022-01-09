
from django.contrib import admin
from django.urls import path
from . import views
 
urlpatterns = [

    path("", views.Anasayfa,name="anasayfa"),
    path("kayıtol/",views.kayıtol,name="kayıtol"),
    path("giris/",views.giris,name="giris"),
    path("cıkıs/",views.cıkıs,name="cıkıs"),
    path("kullancı_kayıtol",views.kullancı_kayıtol,name="kullancı_kayıtol"),
    path("kullancı_giris",views.kullancı_giris,name="kullancı_giris"),

  
]