
from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path("", views.index, name="index"),
    path('search_id/', views.search_id, name='search_id'),
    path('find_password/', views.find_password, name='find_password'),
    path("register/", views.register, name="register"),
    path("login/", views.sign_in, name="login"),
    path('logout/', views.user_logout, name='logout'),
]
