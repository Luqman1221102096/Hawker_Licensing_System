from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('get-content/', views.get_content, name='get_content'),
    path('dashBoard/', views.dashBoard, name='dashBoard'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]
