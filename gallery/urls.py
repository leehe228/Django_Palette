from django.urls import path
from . import views

urlpatterns = [
        path('register/', views.register, name='register'),
        path('getExhibition/', views.getExhibition, name='getExhibition'),
        path('delete/', views.deleteExhibition, name='deleteExhibition'),
        path('create/', views.create, name='create'),
        path('update/', views.update, name='update'),
        path('test/', views.test, name='test'),
       ## path('suggestion/', views.suggestion, name='suggestion'),
        ]
