from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
import os
import random
from django.utils.safestring import mark_safe
from django.shortcuts import redirect

import sys
sys.path.append("..")

from account.models import User
from gallery.models import Exhibition

FILE_PATH = "/home/palette/media/test/"

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
    datas = list()

    for i in l:
        datas.append(str(i.galleryCode))

    random.shuffle(datas)
    datas = datas[:30]

    """dic={}
    for i in l:
        popularity = i.galleryLikes
        gCode = i.galleryCode
        dic[gCode]=popularity
    
    listTuple = sorted(dic.items(), reverse=True, key=lambda item: item[1])
    
    datas = list()"""
    
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
        gCode = i.galleryCode
        dic[gCode]=i.galleryViews

    listTuple = sorted(dic.items(), reverse=True, key=lambda item: item[1])

    datas = list()
    for j in listTuple:
        datas.append(j[0])

    count = 1
    return render(request, '/home/palette/page/templates/page/star.html', {'datas': datas[:20], 'count':count, 'loginedIMG':loginedIMG, 'loginedURL':loginedURL})


''' business page '''
@csrf_exempt
def business(request):
    return render(request, '/home/palette/page/templates/page/main.html', {})


''' saved page  '''
@csrf_exempt
def saved(request):
    email = request.COOKIES.get('userEmail')
    
    alertString = "저장된 전시회가 없습니다. 마음에 드는 전시회를 저장한 후 한 곳에서 모아보세요!"

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
                if len(datas) != 0:
                    alertString = ""

            return render(request, '/home/palette/page/templates/page/saved.html', {'datas':datas, 'alert':alertString})

        except Exception as e:
            print(e)
            return render(request, '/home/palette/page/templates/page/saved.html', {'datas':datas, 'alert':alertString})


''' /search?key= '''
@csrf_exempt
def search(request):

    loginedURL = "http://softcon.ga/login/"
    loginedIMG = "http://141.164.40.63:8000/media/websrc/user_icon.jpg"

    alertString = "검색하신 전시회를 찾을 수 없습니다."

    if request.COOKIES.get('userEmail') != None:
        loginedURL = "http://softcon.ga/setting/"
        loginedIMG = "http://141.164.40.63:8000/media/websrc/setting_icon.jpg"

    keyword = request.GET['key'].strip()

    datas = list()

    if keyword != '':
        l = Exhibition.objects.all()

        # galleryTitle, galleryCreator
        for i in l:
            if CheckSim(i.galleryTitle.strip(), keyword) or CheckSim(i.galleryCreator.strip(), keyword):
                datas.append(i)

        if len(datas) != 0:
            alertString = ""

    if keyword == '':
        alertString = "검색어를 입력하세요."

    return render(request, '/home/palette/page/templates/page/search.html', {'datas':datas, 'alert':alertString, 'keyword':keyword, 'loginedURL':loginedURL, 'loginedIMG':loginedIMG})


@csrf_exempt
def CheckSim(s1, s2):
    count = 0

    for i in s1:
        for j in s2:
            if i == j:
                count += 1

    if count > 0:
        return True
    else:
        return False


''' login page  '''
@csrf_exempt
def login(request):
    email = request.COOKIES.get('userEmail')
    error = ""
    
    if email is None:
        return render(request, '/home/palette/page/templates/page/login.html', {'alert':error})
    else:
        return redirect('home')

@csrf_exempt
def login_e(request):
    email = request.COOKIES.get('userEmail')

    error = "가입되지 않은 계정이거나 비밀번호가 올바르지 않습니다."

    if email is None:
        return render(request, '/home/palette/page/templates/page/login.html', {'alert':error})
    else:
        return redirect('home')


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

    return render(request, '/home/palette/page/templates/page/info.html', {'code':code, 'exhibition':E, 'loginedURL':loginedURL, 'loginedIMG':loginedIMG, 'info':mark_safe(E.galleryInfo)})


''' redirect to '''
@csrf_exempt
def d_redirect(request):
    t = request.GET['to']
    
    # redirect to login
    if t == 'login':
        return login_process(request)

    # redirect to signup
    elif t == 'signup':
        return signup_process(request)

    elif t == 'logout':
        return logout_process(request)

    elif t == 'gallery':
        return gallery(request)

    elif t == 'changepw':
        return change_password_process(request)

    elif t == 'saveprf':
        return save_pref(request)
    
    elif t == 'cancelPay':
        return cancelPayment(request)

    elif t == 'pay':
        return pay_process(request)

    # redirect page not found
    else:
        return HttpResponse("404 Page Not Found")


@csrf_exempt
def pay_process(request):
    email = request.COOKIES.get('userEmail')
    v = request.GET['v']

    user_bp = User.objects.get(userEmail=email)
    user_bp.userPaid = int(v)
    user_bp.save()

    return redirect('setting')


@csrf_exempt
def cancelPayment(request):
    email = request.COOKIES.get('userEmail')

    if email is None:
        return redirect('login')
    else:
        user_bp = User.objects.get(userEmail=email)
        user_bp.userPaid = 0
        user_bp.save()

        return redirect('setting')


@csrf_exempt
def pref(request):
    email = request.COOKIES.get('userEmail')

    if email is None:
        return redirect('login')
    else:
        return render(request, '/home/palette/page/templates/page/edit_pref.html', {})


@csrf_exempt
def save_pref(request):
    email = request.COOKIES.get('userEmail')
    v = request.GET['v']
    
    user_bp = User.objects.get(userEmail=email)
    user_bp.userInterest = v
    user_bp.save()

    return redirect('home')


''' signup page '''
@csrf_exempt
def register(request):
    email = request.COOKIES.get('userEmail')

    if email is None:
        return render(request, '/home/palette/page/templates/page/register.html', {})
    else:
        redirect('home')


@csrf_exempt
def register_e(request):
    email = request.COOKIES.get('userEmail')
    
    error = "이미 가입된 계정입니다."

    if email is None:
        return render(request, '/home/palette/page/templates/page/register.html', {'alert':error})
    else:
        redirect('home')


''' signup processing '''
@csrf_exempt
def signup_process(request):
    email = request.GET['email']
    passwd = request.GET['password']
    name = request.GET['name']
    Age = int(request.GET['age'])
    gender = request.GET['gender']

    if gender == 'M':
        genderValue = 0
    else:
        genderValue = 1

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
    newUser = User(userEmail=email, userPassword=passwd, userName=name, userAge=Age, userCode=PREP + CODE, userSex=gender, userPaid=1)
    try :
        newUser.save(force_insert=True)

        response = redirect('pref')
        response.set_cookie('userEmail', email)

        return response
    except Exception as e:
        print(e)
        return redirect('register_e')
    

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

        return response
    else:
        return redirect('login_e')


''' logout processing '''
@csrf_exempt
def logout_process(request):
    email = request.COOKIES.get('userEmail')

    response = redirect('home')
    response.delete_cookie('userEmail')

    return response


@csrf_exempt
def change_password(request):
    email = request.COOKIES.get('userEmail')

    if email is None:
        return redirect('login')
    else:
        return render(request, '/home/palette/page/templates/page/change_password.html', {})


@csrf_exempt
def change_password_process(request):
    email = request.COOKIES.get('userEmail')
    newPassword = request.GET['password']

    user_bp = User.objects.get(userEmail=email)
    user_bp.userPassword = newPassword
    user_bp.save()

    return redirect('setting')


''' setting page '''
@csrf_exempt
def setting(request):
    username = request.COOKIES.get('userEmail')

    if username is None:
        return redirect('home')
    else:
        userpaid = getPaid(username)
    
        user_bp = User.objects.get(userEmail=username)

        if userpaid == '-1' or userpaid == '0':
            userpaidStr = "구독 전"
        elif userpaid == '1':
            userpaidStr = "정기 구독 중"
        elif userpaid == '2' or userpaid == '3':
            userpaidStr = "구독 중"
        else:
            userpaidStr = ""

        return render(request, '/home/palette/page/templates/page/setting.html', {'user_bp':user_bp, 'paid':userpaidStr})


''' check paid '''
@csrf_exempt
def getPaid(userEmailString):
    try:
        user_bp = User.objects.get(userEmail=userEmailString)
        result = str(user_bp.userPaid)

        return result
    
    except Exception as e:
        print(e)
        return -1


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

        return render(request, '/home/palette/page/templates/page/gallery.html', {'code':code, 'page':page, 'max_page':max_page, 't':t, 'c':mark_safe(c), 'likeIMG':likeIMG, 'likeURL':likeURL})


''' payment page '''
@csrf_exempt
def payment(request):
    
    email = request.COOKIES.get('userEmail')
    
    if email is None:
        return redirect('login')
    else:
        user_bp = User.objects.get(userEmail=email)

        p = user_bp.userPaid

        if p == 0:
            paid = "구독이 필요합니다."
        elif p == 1:
            paid = "정기 구독 중입니다."
        elif p == 2 or p == 3:
            paid = "구독 중입니다."

        return render(request, '/home/palette/page/templates/page/payment.html', {'user':user_bp, 'paid':paid})


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


@csrf_exempt
def private_privacy(request):
    return render(request, '/home/palette/page/templates/page/private_privacy.html', {})
