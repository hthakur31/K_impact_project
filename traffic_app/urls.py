# traffic_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('status/', views.get_status, name='get_status'),
    path('video_feed/', views.video_feed, name='video_feed'),

]
