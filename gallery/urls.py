from django.urls import path
from . import views

urlpatterns = [
        path('register/', views.register, name='register'),
        path('getExhibition/', views.getExhibition, name='getExhibition'),
        path('delete/', views.deleteExhibition, name='deleteExhibition'),
        path('create/', views.create, name='create'),
        path('update/', views.update, name='update'),
        path('getSimpleInfo/', views.getSimpleInfo, name='getSimpleInfo'),
        path('suggestion/', views.suggestion, name='suggestion'),
        path('addLike/', views.addLike, name='addLike'),
        path('cancelLike/', views.cancelLike, name='cancelLike'),
        path('addView/', views.addView, name='addView'),
        path('registerAuction/', views.registerAuction, name='registerAuction'), 
        path('popular/', views.popular, name='popular'),
        path('auctionState/', views.auctionState, name='auctionState'),
        path('auctionStates/', views.auctionStates, name='auctionStates'),
        path('registerAuction/', views.registerAuction, name='registerAuction'),
        path('getAuction/', views.getAuction, name='getAuction'),
        path('auctionProcess/', views.auctionProcess, name='auctionProcess'),
        path('getDate/', views.getDate, name='getDate'),
        path('deleteAuction/', views.deleteAuction, name='deleteAuction'),
        ]
