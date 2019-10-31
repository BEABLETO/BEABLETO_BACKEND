from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    url(r'^signup/$', views.SignUpView.as_view(), name="sign_up"),
    path('token/', views.AuthTokenAPIView.as_view()),
    path('user/', views.UserInfo.as_view())
]