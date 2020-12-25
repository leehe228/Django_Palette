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


''' home page '''
@csrf_exempt
def home(request):
    loginedURL = "http://softcon.ga/login/"
    loginedIMG = "http://141.164.40.63:8000/media/websrc/user_icon.jpg"

    if request.COOKIES.get('userEmail') != None:
        print(request.COOKIES.get('userEmail'))
        loginedIMG = "http://141.164.40.63:8000/media/websrc/setting_icon.jpg"
        loginedURL = "http://softcon.ga/setting/"
    
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


''' hot page '''
@csrf_exempt
def star(request):
    loginedURL = "http://softcon.ga/login/"
    loginedIMG = "http://141.164.40.63:8000/media/websrc/user_icon.jpg"

    if request.COOKIES.get('userEmail') != None:
        print(request.COOKIES.get('userEmail'))
        loginedIMG = "http://141.164.40.63:8000/media/websrc/setting_icon.jpg"
        loginedURL = "http://softcon.ga/setting/"

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


''' business page '''
@csrf_exempt
def business(request):
    return render(request, '/home/palette/page/templates/page/main.html', {})


''' saved page  '''
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
        
            if user_bp.userLike != None:
                userLikeList = user_bp.userLike.split('-')

                for i in userLikeList:
                    j = Exhibition.objects.get(galleryCode=i)
                    datas.append(j)

            return render(request, '/home/palette/page/templates/page/saved.html', {'datas':datas})

        except Exception as e:
            print(e)
            return render(request, '/home/palette/page/templates/page/saved.html', {'datas':datas})


''' /search?key= '''
@csrf_exempt
def search(request):

    loginedURL = "http://softcon.ga/login/"
    loginedIMG = "http://141.164.40.63:8000/media/websrc/user_icon.jpg"

    if request.COOKIES.get('userEmail') != None:
        loginedURL = "http://softcon.ga/setting/"
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


''' login page  '''
@csrf_exempt
def login(request):
    return render(request, '/home/palette/page/templates/page/login.html', {})


''' 404 '''
@csrf_exempt
def no_page(request):
    return render(request, '', {})


''' gallery info page '''
@csrf_exempt
def info(request):
    code = int(request.GET['n'])

    loginedURL = "http://softcon.ga/login/"
    loginedIMG = "http://141.164.40.63:8000/media/websrc/user_icon.jpg"

    if request.COOKIES.get('userEmail') != None:
        loginedURL = "http://softcon.ga/setting/"
        loginedIMG = "http://141.164.40.63:8000/media/websrc/setting_icon.jpg"
    
    E = Exhibition.objects.get(galleryCode=code)

    return render(request, '/home/palette/page/templates/page/info.html', {'code':code, 'exhibition':E, 'loginedURL':loginedURL, 'loginedIMG':loginedIMG})


''' redirect to '''
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


''' signup page '''
@csrf_exempt
def register(request):
    return render(request, '/home/palette/page/templates/page/register.html', {})


''' signup processing '''
@csrf_exempt
def signup_process(request):
    return redirect('home')


''' login processing '''
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


''' logout processing '''
@csrf_exempt
def logout_process(request):
    email = request.COOKIES.get('userEmail')

    response = redirect('home')
    response.delete_cookie('userEmail')

    return response


''' setting page '''
@csrf_exempt
def setting(request):
    username = request.COOKIES.get('userEmail')
    userpaid = getPaid(username)

    if userpaid == False:
        userpaidStr = "구독 결제 전"
    else:
        userpaidStr = "구독 결제 중"

    return render(request, '/home/palette/page/templates/page/setting.html', {'username':username, 'paid':userpaidStr})


''' check paid '''
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


''' gallery page  '''
@csrf_exempt
def gallery(request):
    userEmail = request.COOKIES.get('userEmail')
    
    try:
        to = request.GET['to']
    except Exception as e:
        to = None

    if to == 'c':
        cancelLike(request)
    elif to == 's':
        setLike(request)

    if userEmail == None:
        return redirect('login')

    elif userEmail != None and getPaid(userEmail) == False:
        return redirect('payment')
    
    else:
        code = request.GET['n']
        page = request.GET['p']
        
        E = Exhibition.objects.get(galleryCode=code)

        min_page = 1
        max_page = E.galleryAmount
        
        t = E.titles.split('-')[int(page) - 1]
        c = E.contents.split('-')[int(page) - 1]

        if checkLike(userEmail, code):
            likeIMG = "http://141.164.40.63:8000/media/websrc/r_check_icon.jpg"
            likeURL = "http://softcon.ga/gallery?to=c&n=" + code + "&p=" + page
        else:
            likeIMG = "http://141.164.40.63:8000/media/websrc/r_plus_icon.jpg"
            likeURL = "http://softcon.ga/gallery?to=s&n=" + code + "&p=" + page

        return render(request, '/home/palette/page/templates/page/gallery.html', {'code':code, 'page':page, 'max_page':max_page, 't':t, 'c':c, 'likeIMG':likeIMG, 'likeURL':likeURL})


''' payment page '''
@csrf_exempt
def payment(request):

    return HttpResponse("결제를 해야 합니다.")


''' add like '''
@csrf_exempt
def setLike(request):
    email = request.COOKIES.get('userEmail')
    code = request.GET['n']
    
    user_bp = User.objects.get(userEmail=email)

    if user_bp.userLike == None or user_bp.userLike == '':
        user_bp.userLike = code
    else:
        likeList = user_bp.userLike.split('-')
        likeList.append(code)
        likeString = '-'.join(likeList)
        user_bp.userLike = likeString
    
    user_bp.save()


''' cancel like '''
@csrf_exempt
def cancelLike(request):
    email = request.COOKIES.get('userEmail')
    code = request.GET['n']

    user_bp = User.objects.get(userEmail=email)
    likeList = user_bp.userLike.split('-')
    
    try:
        likeList.remove(code)
    except Exception as e:
        print(e)

    user_bp.userLike = '-'.join(likeList)
    user_bp.save()


''' check like '''
@csrf_exempt
def checkLike(email, code):
    user_bp = User.objects.get(userEmail=email)
    likes = user_bp.userLike
    
    if code in likes:
        return True
    else:
        return False


''' /f?to= '''
@csrf_exempt
def func(request):
    n = request.GET['to']
    
    print(n)

    if n == 'setLike':
        setLike(request)
    
    elif n == 'cancelLike':
        cancelLike(request)

    elif n == 'email':
        pass

    return redirect('close')
    

''' close page with JS '''
@csrf_exempt
def close(request):
    return render(request, '/home/palette/page/templates/page/close.html', {})
