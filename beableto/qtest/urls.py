from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('phone/', views.ret_phone),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('myinfo/', views.GetUserInfoView.as_view(), name='userInfo'),
]