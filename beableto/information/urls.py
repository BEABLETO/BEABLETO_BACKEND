from django.conf.urls import url
from django.urls import path, include
from . import views


urlpatterns = [
    path('save/', views.LocationSaveView.as_view(), name='LSV'),
    path('bussave/', views.BusSaveView.as_view(), name='BSV'),
    path('getinfo/', views.LocationGetView.as_view(), name='LGV'),
    path('getmarker/', views.LocationGetMarkersVIew.as_view(), name="LGM"),
    path('getpath/', views.GetPathsView.as_view(), name='GPV'),
    path('road/', views.RoadSaveView.as_view(), name='RSV'),
    path('basewalk/', views.GetBaseWalkView.as_view(), name='GBWV'),
    path('getpaths/', views.GetPathsView.as_view(), name='GPV'),
    path('getallmarkers/', views.LocationGetAllMarkersVIew.as_view(), name='MGAV'),
    path('savepose/', views.CurPoseSaveView.as_view(), name='CPSV'),
    path('getpose/', views.GetPositionsView.as_view(), name='GPV'),
    path('getfragment/', views.GetFragmentsView.as_view(), name='GFV'),
]