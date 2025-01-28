from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('get-content/', views.get_content, name='get_content'),
    path("dashBoard/", views.getDashBoard, name="getDashBoard")
]
