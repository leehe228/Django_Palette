from django.urls import path
from . import views

urlpatterns = [
    path('business/', views.business, name='business'),     
    path('home/', views.home, name='home'),
    path('star/', views.star, name='star'),
    path('saved/', views.saved, name='saved'),
    path('search/', views.search, name='search'),
    path('login/', views.login, name='login'),
    path('redirect/', views.d_redirect, name='redirect'),
    path('info/', views.info, name='info'),
    path('setting/', views.setting, name='setting'),
    path('gallery/', views.gallery, name='gallery'),
    path('payment/', views.payment, name='payment'),
]
