from django.conf.urls import url
from django.urls import path, include
from . import views


urlpatterns = [
    path('save/', views.LocationSaveView.as_view(), name='LSV'),
]