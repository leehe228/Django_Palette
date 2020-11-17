from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
import random
import csv
import os
import shutil
import random

FILE_PATH = "/home/palette/media/test/"

@csrf_exempt
def mkUserCode():
    f = open(FILE_PATH + "userCode.txt", 'r')
    line = f.read()
    if (line==''):
        line = '0'
    CODE = int(line) + 1
    f.close()

    f = open(FILE_PATH + "userCode.txt", "w")
    f.write(str(CODE))

    return str(CODE)

@csrf_exempt
def signup(request):
    Email = request.POST.get('email')
    Password = request.POST.get('password')
    Name = request.POST.get('name')
    Age = request.POST.get('age') 
    gender = "UNKNOWN"

    CODE = mkUserCode()
    l = ['A','R','T','I','S','L','O','V','E']

    if (int(Age) > 89):
        Age = "89"
    PREP = l[int(Age) // 10]

    if(gender == "UNKNOWN"):
        PREP = PREP + "U"
    elif(gender == "MAN"):
        PREP = PREP + "M"
    elif(gender == "WOMAN"):
        PREP = PREP + "W"
    
    #객체 인스턴스화
    newUser = User(userEmail=Email, userPassword=Password, userName=Name, userAge=Age, userCode=PREP + CODE, userSex=gender)
    try :
        newUser.save(force_insert=True)
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse('-1')


@csrf_exempt
def login(request):
    Email = request.POST.get('email')
    Password = request.POST.get('password')

    queryset = User.objects.filter(userEmail=Email, userPassword=Password)
    query = User.objects.all()

    if (queryset):
        return HttpResponse('1')
    else:
        return HttpResponse('-1')


@csrf_exempt
def hello(request):
    test = request.POST.get('test')
    return HttpResponse("Hello")


@csrf_exempt
def ask(request):
    email = request.POST.get('email')
    title = request.POST.get('title')
    content = request.POST.get('content')
    
    print(email, title, content)

    emailTitle = "palette 문의사항 접수 안내"

    email = EmailMessage(emailTitle, "제목 : " + title + "\n본문 : " + content + "\n\n위와 같은 내용으로 문의사항이 접수되었습니다. 감사합니다.", to=[email])

    try:
        email.send()
        return HttpResponse("1")
    except Exception as e:
        print(e)
        return HttpResponse("-1")


@csrf_exempt
def sendCode(request):
    title = "[Palette] Please verify your account"
    content1 = "Your verifying numbere is ["
    content2 = "] Please enter this number correctly on the app. Thanx:)"

    CODE = random.randrange(100000,1000000)
    Email = request.POST.get('email')

    email = EmailMessage(title, content1 + str(CODE) + content2, to = [Email])
    try :
        print("CODE is " + str(CODE))
        email.send()
        return HttpResponse(str(CODE))
    except Exception as e:
        print(e)
        return HttpResponse('-1')


@csrf_exempt
def setInterest(request):
    Email = request.POST.get('email')
    Interest = request.POST.get('interest')

    try:
        user_bp = User.objects.get(userEmail=Email)
        user_bp.userInterest = Interest
        user_bp.save()
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse('-1')


@csrf_exempt
def getInfo(request):
    Email = request.POST.get('email')
    
    try :
        user_bp = User.objects.get(userEmail=Email)
        result = user_bp.userName + "&" + str(user_bp.userAge) + "&" + user_bp.userInterest
        return HttpResponse(result)
    except Exception as e:
        print(e)
        return HttpResponse('-1')


@csrf_exempt
def getLike(request):
    Email = request.POST.get('email')
    user_bp = User.objects.get(userEmail=Email)
    return HttpResponse(user_bp.userLike)
        

@csrf_exempt
def setLike(request):
    Email = request.POST.get('email')
    UserLike = request.POST.get('userLike')

    try:
        user_bp = User.objects.get(userEmail=Email)
        user_bp.userLike = UserLike
        user_bp.save()
        return HttpResponse("1")
    except Exception as e:
        print(e)
        return HttpResponse("-1")


@csrf_exempt
def changePassword(request):
    Email = request.POST.get('email')
    oldPassword = request.POST.get('oldPassword')
    newPassword = request.POST.get('newPassword')

    queryset = User.objects.filter(userEmail=Email, userPassword=oldPassword)
    query = User.objects.all()

    if (queryset):
        try :
            user_bp = User.objects.get(userEmail=Email)
            user_bp.userPassword = newPassword
            user_bp.save()
            return HttpResponse('1')
        except Exception as e:
            print(e)
            return HttpResponse('-1')        
    else:
        return HttpResponse('-1')


@csrf_exempt
def deleteAccount(request):
    Email = request.POST.get('email')
    Password = request.POST.get('password')

    queryset = User.objects.filter(userEmail=Email, userPassword=Password)
    query = User.objects.all()

    if (queryset):
        try :
            uesr_bp = User.objects.get(userEmail=Email)
            user_bp.delete()
            print("suc")
            return HttpResponse('1')
        except Exception as e:
            print(e)
            print("fail")
            return HttpResponse('-1')
    else:
        print("no matching User")
        return HttpResponse('-1')
    

@csrf_exempt
def changeInfo(request):
    Email = request.POST.get('email')
    Name = request.POST.get('name')
    Age = request.POST.get('age') 

    try:
        user_bp = User.objects.get(userEmail=Email)
        user_bp.userName = Name
        user_bp.userAge = Age
        user_bp.save()
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse('-1')



# Create your views here.
