from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('get-content/', views.get_content, name='get_content'),
    path('dashBoard/', views.dashBoard, name='dashBoard'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('viewLicense/', views.viewLicense, name='viewLicense'),
    path('revokeLicense/', views.revokeLicense, name='revokeLicense'),
    path('licensePage/<str:key_id>/', views.licensePage, name='licensePage'),
    path('storeReport/<str:key_id>/', views.storeReport, name='storeReport'),
    path('note/<str:key_id>/', views.note, name='note'),
    path('storeNote/<str:key_id>/', views.storeNote, name='storeNote'),
    path('revokeRequests', views.revokeRequests, name='revokeRequests'),
    path('revokeApproval/<str:key_id>/', views.revokeApproval, name='revokeApproval'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
