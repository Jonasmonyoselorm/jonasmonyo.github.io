from django.urls import path
from . import views

app_name = "event"
urlpatterns = [
    path('', views.index, name="index"),

    # using path convertors like 
    # "int: numbers, str: strings, path: whole urls/, 
    # slug: hyphen- and _underscores, UUID: universally unique identifier"***
    path('<int:year>/<str:month>/', views.index, name="index"), 
]