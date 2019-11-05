from django.conf.urls import url
from django.urls import path, include
from . import views


urlpatterns = [
    path('save/', views.LocationSaveView.as_view(), name='LSV'),
    path('bussave/', views.BusSaveView.as_view(), name='BSV'),
    path('getinfo/', views.LocationGetView.as_view(), name='LGV'),
    path('getmarker/', views.LocationGetMarkers.as_view(), name="LGM"),
    path('getpath/', views.GetPathsView.as_view(), name='GPV'),
    path('road/', views.RoadSaveView.as_view(), name='SR')
]