from django.urls import path
from . import views

urlpatterns = [
        path('', views.hello, name='hello'),
        path('login/', views.login, name='login'),
        path('signup/', views.signup, name='signup'),
        path('sendCode/', views.sendCode, name='sendCode'),
        path('setInterest/', views.setInterest, name='setInfo'),
        path('getInfo/', views.getInfo, name='getInfo'),
        path('changePassword/', views.changePassword, name='changePassword'),
        path('deleteAccount/', views.deleteAccount, name='deleteAccount'),
        path('ask/', views.ask, name='ask'),
        path('changeInfo/', views.changeInfo, name='changeInfo'),
        path('mkUserCode/', views.mkUserCode, name='mkUserCode'),
        path('setLike/', views.setLike, name='setLike'),
        path('getLike/', views.getLike, name='getLike'),
        ]
