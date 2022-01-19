from logging import exception
from django.shortcuts import render,redirect

from django.http import HttpResponse
import pyrebase
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from lcu_driver import Connector
import psutil
import requests

from requests.auth import HTTPBasicAuth
import json




# Create your views here.


config={
  "apiKey": "AIzaSyAwH2uSz9iiUTBa8W4NMf-3Osu7spMmbz4",
  "authDomain": "django-c0d88.firebaseapp.com",
  "databaseURL": "https://django-c0d88-default-rtdb.firebaseio.com",
  "projectId": "django-c0d88",
  "storageBucket": "django-c0d88.appspot.com",
  "messagingSenderId": "290546126178",
  "appId": "1:290546126178:web:68e8cefcd33dbf6259b03b",
  "measurementId": "G-F5G1043X39"
  
}

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()

        



def Home(request):
    #DATABASE VERİLERİ
    format= database.child("users").get(token="Oq4fBRRrJEohuwo9J7pd63q3aH5buH50DHCpJxjt")
    Database_All_Data_Value=format.val()
    return render(request,"index.html",{"Data_For_User":Database_All_Data_Value})

def SignUp(request):
    if request.user.is_authenticated:
        return redirect('Home')
    if request.method == "POST":
        is_Active=False
        lol_nickname="None"

        name=request.POST.get("name")
        email=request.POST.get("email")
        password=request.POST.get("password")

        try:
            #KULLANICI KAYIT OLMA SQLİTE
            try:
                user=User.objects.create_user(str(name), str(email), str(password))
                user.save()
                try:
                 #KULLANICI KAYDETME FİREBASE
                    id=user.id
                    data = {"id":id,"name":name,"email":email,"password":password,"is_Active":is_Active,"lol_nickname":lol_nickname}
                    database.child("users").push(data)
                    authe.create_user_with_email_and_password(email,password)
                    try:
                        print("kayıt başarılı")
                        return redirect("login")
                        

                    except Exception as e:
                        print(str(e)+"login sayfa hatası")


                except Exception as e:
                    print(str(e)+"FİREBASE  HATA")
                

            except Exception as e:
                print(str(e)+"SQLİTE HATA")
 
        except Exception as e:
            print(str(e)+"POST HATA")
    return render(request,"sign-up.html")




def login_page(request):
    if request.user.is_authenticated:
        return redirect('Home')

    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        #FİREBASE KULLANICI DATA GETİRME
        try:
            all_users = database.child("users").get(token="Oq4fBRRrJEohuwo9J7pd63q3aH5buH50DHCpJxjt")
            #kullanıcı emailine göre kullanıcı adı bulma
            try:
                for user in all_users.each():
                    firebase_email=user.val()["email"]
                    name_key=user.key()
                    firebase_email=str(firebase_email)
                    if firebase_email == str(email):
                        firebase_name=user.val()["name"]
                        #kullanıcı doğrulama
                        try:
                            user = authenticate(request, username=str(firebase_name), password=str(password))
                            
                            login(request,user)
                            try:
                                authe.sign_in_with_email_and_password(email,password)
                                try:
                                    database.child("users").child(name_key).update({"is_Active": "True"})
                                    try:
                                     return redirect("Home")
                                    except Exception as e:
                                        print(str(e)+"HOME SAYFASINA GİTMİYOR")
                                except Exception as e:
                                    print(str(e)+"FİREBASE İS_ACTİVE DEĞİŞTİRİLEMİYOR")
                            except Exception as e:
                                print(str(e)+"KULLANICI  FİREBASE  ONAYLAMIYOR")
                        except Exception as e:
                            print(str(e)+"KULLANICI  SQLİTE  ONAYLAMIYOR")
            except Exception as e:
                print(str(e)+"FİREBASE DATALARI GELMİYOR")   
        except Exception as e:
            print(str(e)+"FİREBASE DATALARI GELMİYOR")
    return render(request,"log-in.html")


def logout_page(request):
    format= database.child("users").get(token="Oq4fBRRrJEohuwo9J7pd63q3aH5buH50DHCpJxjt")
    id=request.user.id
    
    for i in format:
        
        if i.val()["id"] == id:
            a=i.key()
            database.child("users").child(a).update({"is_Active": "False"})
            logout(request)    
            return redirect('Home')



@csrf_exempt
def ContentLol(request):
    if request.method =="POST":
        ip=request.META.get("HTTP_X_FORWARDED_FOR")
        format= database.child("users").get(token="Oq4fBRRrJEohuwo9J7pd63q3aH5buH50DHCpJxjt")
        id=request.user.id
        
        for i in format:
            
            if i.val()["id"] == id:
                a=i.key()
                database.child("users").child(a).update({"button": "True","ip":ip})


    
        


def User_Challenge(request):
    istek_alan = request.GET.get('abc')
    istek_gönderen_id=request.user.id
    istek_gönderen=request.user.username

    #nicke göre id getirme firebase
    format= database.child("users").get(token="Oq4fBRRrJEohuwo9J7pd63q3aH5buH50DHCpJxjt")
    for i in format.each():
        
        if i.val()["name"] == istek_alan:
            istek_alan_id=i.val()["id"]
            data = {
                "istek_gönderen":istek_gönderen,
                "istek_gönderen_id":istek_gönderen_id,
                "istek_alan":istek_alan,
                "istek_alan_id":istek_alan_id,
                "istek_onay":"True"}
            database.child("istekler").push(data)










    

    

 
    return redirect("ContentLol")
