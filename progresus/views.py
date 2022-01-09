from django.shortcuts import render,redirect

from django.http import HttpResponse
import pyrebase
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt



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

        












def Anasayfa(request):
    format= database.child("users").get()
    aa=format.val()



    return render(request,"anasayfa.html",{"forr":aa})
 
def kayıtol(request):
    return render(request,"kayıtol.html")
def giris(request):
    return render(request,"giris.html")
def icerik(request):
    return render(request,"icerik.html")

def kullancı_kayıtol(request):
    isim=request.POST.get("isim")
    
    is_Active=False
    email=request.POST.get("email")

    sifre=request.POST.get("sifre")
    # format= database.child("users").get()
    # aa=format.val()
    # id=int(len(aa))+1
    # id=str(id)

    
    
    try:
        user=User.objects.create_user(str(isim), str(email), str(sifre))
        
        user.save()
        id=user.id
        data = {"id":id,"name":isim,"email":email,"password":sifre,"is_Active":is_Active}
        database.child("users").push(data)
        

        authe.create_user_with_email_and_password(email,sifre)
    except:
        return HttpResponse("kayıtolma başarısız")
    return redirect("giris")


@csrf_exempt 
def kullancı_giris(request):

    format= database.child("users").get()
    aa=format.val()


    
    email=request.POST.get("email")
    sifre=request.POST.get("sifre")
 
    try:
        
        all_users = database.child("users").get()
        for user in all_users.each():
            user_email=user.val()["email"]
            key_is_Activate=user.key()
            user_email=str(user_email)
            
            if user_email == str(email):
                
                user_login=user.val()["name"]
                print(user_login)
                user = authenticate(request, username=user_login, password=sifre)
                login(request,user)
                # authe.sign_in_with_email_and_password(email,sifre)
                database.child("users").child(key_is_Activate).update({"is_Active": "True"})
                



    except:
        return render(request,"anasayfa.html",{"forr":aa})
    return render(request,"anasayfa.html",{"forr":aa})

def cıkıs(request):
    format= database.child("users").get()
    id=request.user.id
    
    for i in format:
        
        if i.val()["id"] == id:
            a=i.key()
            database.child("users").child(a).update({"is_Active": "False"})
            logout(request)    
            return redirect('giris')
            
