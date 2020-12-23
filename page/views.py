from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
import os
import random

from django.shortcuts import redirect

import sys
sys.path.append("..")

from account.models import User
from gallery.models import Exhibition


@csrf_exempt
def home(request):
    loginedURL = "http://softcon.ga/web/login/"
    loginedIMG = "http://141.164.40.63:8000/media/websrc/user_icon.jpg"

    if request.COOKIES.get('userEmail') is not None:
        print(request.COOKIES.get('userEmail'))
        loginedIMG = "http://141.164.40.63:8000/media/websrc/setting_icon.jpg"
        loginedURL = "http://softcon.ga/web/setting/"
    
    l = Exhibition.objects.all()
    dic={}
    for i in l:
        popularity = i.galleryLikes
        gCode = i.galleryCode
        dic[gCode]=popularity

    listTuple = sorted(dic.items(), reverse=True, key=lambda item: item[1])
    
    datas = list()
    for j in listTuple:
        #datas.append("http://141.164.40.63:8000/media/database/" + str(j[0]) + "/" + str(random.randrange(1, 4)) + ".jpg")
        datas.append(j[0])
    return render(request, '/home/palette/page/templates/page/home.html', {'datas': datas, 'loginedIMG':loginedIMG, 'loginedURL':loginedURL})


@csrf_exempt
def star(request):
    loginedURL = "http://softcon.ga/web/login/"
    loginedIMG = "http://141.164.40.63:8000/media/websrc/user_icon.jpg"

    if request.COOKIES.get('userEmail') is not None:
        print(request.COOKIES.get('userEmail'))
        loginedIMG = "http://141.164.40.63:8000/media/websrc/setting_icon.jpg"
        loginedURL = "http://softcon.ga/web/setting/"

    l = Exhibition.objects.all()
    dic={}
    for i in l:
        popularity = i.galleryLikes
        gCode = i.galleryCode
        dic[gCode]=popularity

    listTuple = sorted(dic.items(), reverse=True, key=lambda item: item[1])

    datas = list()
    for j in listTuple:
        datas.append(j[0])
    return render(request, '/home/palette/page/templates/page/star.html', {'datas': datas, 'loginedIMG':loginedIMG, 'loginedURL':loginedURL})


@csrf_exempt
def main(request):
    return render(request, '/home/palette/page/templates/page/main.html', {})


@csrf_exempt
def saved(request):
    return render(request, '/home/palette/page/templates/page/saved.html', {})


@csrf_exempt
def search(request):
    keyword = request.GET['key'].strip()

    datas = list()

    if not keyword is '':
        l = Exhibition.objects.all()

        # galleryTitle, galleryCreator
        for i in l:
            if i.galleryTitle.strip() in keyword or keyword in i.galleryTitle.strip() or i.galleryCreator.strip() in keyword or keyword in i.galleryCreator.strip():
                datas.append(i)

    return render(request, '/home/palette/page/templates/page/search.html', {'datas':datas})


@csrf_exempt
def login(request):
    return render(request, '/home/palette/page/templates/page/login.html', {})


@csrf_exempt
def no_page(request):
    return render(request, '', {})


@csrf_exempt
def info(request):
    n = request.GET['n']

    imgurl = "http://141.164.40.63:8000/media/database/" + n + "/1.jpg"
    
    return HttpResponse(imgurl)
    # return render(request, '/home/palette/page/templates/page/info.html', {"image":imgurl})


@csrf_exempt
def d_redirect(request):
    t = request.GET['to']
    
    # redirect to login
    if t == 'login':
        return login_process(request)

    # redirect to signup
    elif t == 'register':
        return signup_process(request)

    elif t == 'logout':
        return logout_process(request)

    # redirect page not found
    else:
        return HttpResponse("404 Page Not Found")


@csrf_exempt
def signup_process(request):
    return HttpResponse('not found')


@csrf_exempt
def login_process(request):
    email = request.GET['email']
    passwd = request.GET['password']
    
    queryset = User.objects.filter(userEmail=email, userPassword=passwd)
    
    if (queryset):
        # save cookie
        response = redirect('home')
        response.set_cookie('userEmail', email)

        # return HttpResponse(str("login success! : emailAddress : " + email + ", password : " + passwd))
        return response
    else:
        # return redirect('login')
        return HttpResponse(str("login failed! : emailAddress : " + email + ", password : " + passwd))


@csrf_exempt
def login_process(request):
    email = request.COOKIES.get('userEmail')

    response = redirect('home')
    response.delete_cookie('userEmail')

    return response

@csrf_exempt
def setting(request):
    return HttpResponse(request.COOKIES.get('userEmail'))
