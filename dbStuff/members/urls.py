from django.urls import path
from . import views

app_name = 'members'
urlpatterns = [
    path('login_user/', views.loginPage, name='login-Page'),
    path('logout_user/', views.logOutPage, name='logout-Page'),
    path('register_user/', views.registerUser, name='register-user'),


]
