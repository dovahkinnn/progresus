from logging import exception
from django.shortcuts import render,redirect

from django.http import HttpResponse
import pyrebase
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from lcu_driver import Connector



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
    format= database.child("users").get()
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
            all_users = database.child("users").get()
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
    format= database.child("users").get()
    id=request.user.id
    
    for i in format:
        
        if i.val()["id"] == id:
            a=i.key()
            database.child("users").child(a).update({"is_Active": "False"})
            logout(request)    
            return redirect('Home')



@csrf_exempt
def ContentLol(request):
    connector = Connector()

    # Creates 5v5 Practice Tool
    async def createLobby(connection):
        data = {
            "customGameLobby": {
                "configuration": {
                    "gameMode": "PRACTICETOOL",
                    "gameMutator": "",
                    "gameServerRegion": "",
                    "mapId": 11,
                    "mutators": {
                        "id": 1
                    },
                    "spectatorPolicy": "AllAllowed",
                    "teamSize": 5,
                },
                "lobbyName": "League of Poro's Practice Tool",
                "lobbyPassword": ""
            },
            "isCustom": True,
        }
        # make the request to switch the lobby
        lobby = await connection.request('post', '/lol-lobby/v2/lobby', data=data)

        # if HTTP status code is 200 the lobby was created successfully
        if lobby.status == 200:
            print('The lobby was created correctly')
        else:
            print('Whops, Yasuo died again.')


    # Contacts LCU API to add bots
    async def executeAddBot(connection, data):
        res = await connection.request('post', '/lol-lobby/v1/lobby/custom/bots', data=data)
        if res.status == 204:
            print('Bot added')
        else:
            print('Whops, Yasuo died again.')

    # Selects which bots to add and adds them to an existing lobby
    async def addBots(connection):
        ids = [1, 3, 8, 10, 11]

        # add bots to the player's team
        for id in ids[:4]:
            data = {
                "botDifficulty": "EASY",
                "championId": id,
                "teamId": "100"
            }
            await executeAddBot(connection, data)

        # add bots to the opposite team
        for id in ids:
            data = {
                "botDifficulty": "EASY",
                "championId": id,
                "teamId": "200"
            }
            await executeAddBot(connection, data)


    # fired when LCU API is ready to be used
    @connector.ready
    async def connect(connection):
        print('LCU API is ready to be used.')

        # check if the user is already logged into his account
        summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
        if summoner.status != 200:
            print('Please login into your account.')
        else:
            print('Switching the lobby type.')
            await createLobby(connection)
            await addBots(connection)


    # fired when League Client is closed (or disconnected from websocket)
    @connector.close
    async def disconnect(_):
        print('The client have been closed!')

    # starts the connector
    connector.start()
  
  
  

    return redirect('Home')

def User_Challenge(request):
  
    istek_alan = request.GET.get('abc')
    istek_gönderen_id=request.user.id
    istek_gönderen=request.user.username

    #nicke göre id getirme firebase
    format= database.child("users").get()
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
