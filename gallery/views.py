from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from .models import Exhibition
from django.views.decorators.csrf import csrf_exempt
import os
import shutil
import json
from PIL import Image
from datetime import datetime
from .models import Images
from django.shortcuts import render

FILE_PATH = "/home/palette/media/test/"
IMAGE_PATH = "/home/palette/media/temp/"    
DATA_PATH = "/home/palette/media/database/"

# 삭제
@csrf_exempt
def deleteExhibition(request):
    pass


# json Update
@csrf_exempt
def update(request):
    j = open(FILE_PATH + "database.json", encoding="utf-8-sig")
    newList = {}
    newList["DATA"] = []

    try:
        json_data = json.loads(j.read())
        print(json_data["DATA"])
        now = datetime.now()
        date_time = now.strftime("%Y%m%d")

        for i in range (len(json_data["DATA"])):
            print(json_data["DATA"][i]["DUEDATE"], end = ' ')

            if (int(json_data["DATA"][i]["DUEDATE"])) >= (int(date_time)):
                newList["DATA"].append(json_data["DATA"][i])

    except Exception as e:
        print(e)

    j.close()

    with open(FILE_PATH + 'database.json', 'w', encoding='UTF-8-sig') as f:
        f.write(json.dumps(newList, ensure_ascii=False, indent=4))
    
    print("Done.")

    return HttpResponse("Updated Successfully")

# 전시회 정보 반환
@csrf_exempt
def getExhibition(request):
    code = request.POST.get("code")
    bp = Exhibition.objects.get(galleryCode = code)
    data = bp.galleryTitle + "&" + bp.galleryCreator+"&" + bp.galleryInfo + "&" +str(bp.galleryAmount) + "&" + bp.titles +"&"+ bp.contents + "&"+ bp.dueDate + "&"+ bp.category
    bp.save()
    
    try :
        return HttpResponse(data)
    except Exceptions as e:
        print(e)
        return HttpResponse('-1')
    


# 전시회 정보 저장
@csrf_exempt
def register(request):
    GalleryTitle = request.POST.get('galleryTitle')
    GalleryCreator = request.POST.get('galleryCreator')
    GalleryInfo = request.POST.get('galleryInfo')
    DueDate = request.POST.get('dueDate')
    Category = request.POST.get('category')
    
    # 코드 생성
    CODE = makeCode()
    createDir(CODE)

    j = open(FILE_PATH + "database.json", encoding="utf-8-sig")
    newList = {}
    newList["DATA"] = []

    try:
        json_data = json.loads(j.read())
        print(json_data["DATA"])
        now = datetime.now()
        date_time = now.strftime("%Y%m%d")

        for i in range (len(json_data["DATA"])):
            print(json_data["DATA"][i]["DUEDATE"], end = ' ')
        
            if (int(json_data["DATA"][i]["DUEDATE"])) >= (int(date_time)):
                newList["DATA"].append(json_data["DATA"][i])
    except Exception as e:
	    print(e)

    dictToAdd = {"CODE":CODE, "TITLE":GalleryTitle, "CREATOR":GalleryCreator, "INFO":GalleryInfo, "AMOUNT":"0", "ARTTITLES":"", "ARTCONTENTS":"", "DUEDATE":str(DueDate), "CATEGORY":Category}

    newList["DATA"].append(dictToAdd)
    j.close()
   
    print(newList)

    with open(FILE_PATH + 'database.json', 'w', encoding='UTF-8-sig') as f:
        f.write(json.dumps(newList, ensure_ascii=False, indent=4))

    newExhibition = Exhibition(galleryCode=CODE, galleryTitle=GalleryTitle, galleryCreator=GalleryCreator, galleryInfo=GalleryInfo, galleryAmount="0", titles="", contents="", dueDate=DueDate, category=Category)

    try :
        newExhibition.save(force_insert=True)
        update()
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse('-1')


#exhibition 코드 생성
def makeCode():
    f = open(FILE_PATH + "galleryCode.txt", 'r')
    line = f.read()
    if (line == ''):
        line = '0'
    CODE = int(line) + 1
    f.close()

    f = open(FILE_PATH + "galleryCode.txt", 'w')
    f.write(str(CODE))

    return str(CODE)


@csrf_exempt
def create (request):
    code = request.POST.get("code")
    image_list = request.FILES.getlist("image")
    titles = request.POST.get("titles")
    contents = request.POST.get("contents")

    print(code)
    for item in image_list:
        images = Images.objects.create(photo=item)
        images.save()

    file_list = os.listdir(IMAGE_PATH)
    bp = Exhibition.objects.get(galleryCode = code)
    bp.galleryAmount = str(int(bp.galleryAmount) + 1)
    if (bp.galleryAmount == '1') :
        bp.titles = titles
        bp.contents = contents
    else :
        bp.contents = bp.contents + "-" + contents
        bp.titles = bp.titles + "-" + titles
    
    bp.save()

    # imageName = os.path.splitext(IMAGE_PATH + galleryCode + ".jpg")
    # print(imageName)
    
    fileName = bp.galleryAmount + ".jpg"
    shutil.move(IMAGE_PATH + file_list[0], DATA_PATH +code+"/"+ fileName )

    return HttpResponse("1")


def createDir(code):
    try:
        if not os.path.exists(DATA_PATH + code + "/" ):
            os.makedirs(DATA_PATH + code + "/")
    except OSError:
        print("Directory Already Exists!")


@csrf_exempt
def test(request):
    l = Exhibition.objects.all()

    for i in l:
        print(i.category)

    
