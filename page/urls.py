from django.urls import path
from . import views

urlpatterns = [
    path('clear/', views.clearViews, name='clear'),     
    path('', views.home, name='home'),
    path('star/', views.star, name='star'),
    path('saved/', views.saved, name='saved'),
    path('search/', views.search, name='search'),
    path('login/', views.login, name='login'),
    path('redirect/', views.d_redirect, name='redirect'),
    path('info/', views.info, name='info'),
    path('setting/', views.setting, name='setting'),
    path('gallery/', views.gallery, name='gallery'),
    path('payment/', views.payment, name='payment'),
    path('f/', views.func, name='func'),
    path('close/', views.close, name='close'),
    path('register/', views.register, name='register'),
    path('pref/', views.pref, name='pref'),
    path('login_e/', views.login_e, name='login_e'),
    path('register_e/', views.register_e, name='register_e'),
    path('private_privacy/', views.private_privacy, name='private_privacy'),
]
