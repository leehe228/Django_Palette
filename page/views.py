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

    if request.COOKIES.get('userEmail') != None:
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

    if request.COOKIES.get('userEmail') != None:
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


''' /web/business/ '''
@csrf_exempt
def business(request):
    return render(request, '/home/palette/page/templates/page/main.html', {})


''' /web/saved/ '''
@csrf_exempt
def saved(request):
    email = request.COOKIES.get('userEmail')
    
    if email is None:
        return redirect('login')
    else:
        
        userLikeList = list()
        datas = list()
        try:
            user_bp = User.objects.get(userEmail=email)
            E = Exhibition.objects.all()
        
            if user_bp.userLike != None:
                userLikeList = user_bp.userLike.split('-')

                for i in userLikeList:
                    for j in E:
                        if i == str(j.galleryCode):
                            datas.append(j)

            return render(request, '/home/palette/page/templates/page/saved.html', {'datas':datas})

        except Exception as e:
            print(e)
            return HttpResponse("Page Load Fault")


''' /web/search?key= '''
@csrf_exempt
def search(request):

    loginedURL = "http://softcon.ga/web/login/"
    loginedIMG = "http://141.164.40.63:8000/media/websrc/user_icon.jpg"

    if request.COOKIES.get('userEmail') != None:
        loginedURL = "http://softcon.ga/web/setting/"
        loginedIMG = "http://141.164.40.63:8000/media/websrc/setting_icon.jpg"

    keyword = request.GET['key'].strip()

    datas = list()

    if keyword != '':
        l = Exhibition.objects.all()

        # galleryTitle, galleryCreator
        for i in l:
            if i.galleryTitle.strip() in keyword or keyword in i.galleryTitle.strip() or i.galleryCreator.strip() in keyword or keyword in i.galleryCreator.strip():
                datas.append(i)

    return render(request, '/home/palette/page/templates/page/search.html', {'datas':datas, 'keyword':keyword, 'loginedURL':loginedURL, 'loginedIMG':loginedIMG})


''' /web/login/ '''
@csrf_exempt
def login(request):
    return render(request, '/home/palette/page/templates/page/login.html', {})


@csrf_exempt
def no_page(request):
    return render(request, '', {})


@csrf_exempt
def info(request):
    code = int(request.GET['n'])
    title = "title"
    content = "content"
    return render(request, '/home/palette/page/templates/page/info.html', {'code':code, 'title':title, 'content':content})


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

    elif t == 'gallery':
        return gallery(request)

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
def logout_process(request):
    email = request.COOKIES.get('userEmail')

    response = redirect('home')
    response.delete_cookie('userEmail')

    return response


@csrf_exempt
def setting(request):
    username = request.COOKIES.get('userEmail')
    userpaid = getPaid(username)

    if userpaid == False:
        userpaidStr = "구독 결제 전"
    else:
        userpaidStr = "구독 결제 중"

    return render(request, '/home/palette/page/templates/page/setting.html', {'username':username, 'paid':userpaidStr})


@csrf_exempt
def getPaid(userEmailString):
    try:
        user_bp = User.objects.get(userEmail=userEmailString)
        result = str(user_bp.userPaid)

        if result == '0':
            return False
        else:
            return True
    
    except Exception as e:
        print(e)
        return False


@csrf_exempt
def gallery(request):
    userEmail = request.COOKIES.get('userEmail')

    if userEmail == None:
        return redirect('login')

    elif userEmail != None and getPaid(userEmail) == False:
        return redirect('payment')
    
    else:
        code = request.GET['n']
        page = request.GET['p']

        min_page = 1
        max_page = 10
        
        return render(request, '/home/palette/page/templates/page/gallery.html', {'code':code, 'page':page})


@csrf_exempt
def payment(request):

    return HttpResponse("결제를 해야 합니다.")
