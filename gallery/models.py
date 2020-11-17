from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField


class Exhibition(models.Model):
    # 전시회 제목
    galleryTitle = models.CharField(max_length=100)
    # 전시회 작가
    galleryCreator = models.CharField(max_length=30, default='')
    # 전시회 설명
    galleryInfo = models.CharField(max_length=300, default='')
    # 전시회 고유 코드, 검색 시 사용
    galleryCode = models.IntegerField(primary_key=True, default=-1, null=False, unique=True, db_index=True)
    # 전시회 개수 
    galleryAmount = models.IntegerField(default=0)
    # 작품 제목(&)
    titles = models.TextField(default='')
    # 작품 설명(&)
    contents = models.TextField(default='')
    # 마감 날짜(&)
    dueDate = models.CharField(max_length=8, default='20000000')
    # 전시회 카테고리
    category = models.CharField(max_length=20, default='000000000')


    # 파일 관련
    def __str__(self):
        return str(self.galleryCode)

class Images(models.Model):
    photo = ProcessedImageField(
            upload_to = 'temp',
            format = 'JPEG',
            options = {'quality':60},
            null=True)

class Auction(models.Model):
    #경매 시작가
    startPrice = models.IntegerField(default=0)
    #새로운 입찰가
    newPrice = models.IntegerField(default=0)
