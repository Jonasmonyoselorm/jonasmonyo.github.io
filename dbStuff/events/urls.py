from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.all_events, name='list-events'),
]