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
    path('upload/', views.file_upload_view, name='file_upload'),
    path('files/', views.file_list_view, name='file_list'),
    path('viewFormManager/', views.viewFormManager, name='viewFormManager'),
    path('viewValidated/', views.viewValidated, name='viewValidated'),
    path('applicationApproval/', views.applicationApproval, name='applicationApproval'),
    #l
    path("hawker-menu/", views.hawker_menu, name="hawker_menu"),
    path("apply/", views.apply_license, name="apply_license"),
    path("document-verification/", views.document_verification, name="document_verification"),
    path('success/', views.success, name='success'),
    path('logout/', views.logout_view, name='logout'),  
    path('status/', views.check_status, name='check_status'),
    path('renew/', views.renew_license, name='renew_license'),
    path('payment/', views.payment, name='payment'),
    path('payment/success/', views.pay_success, name='pay_success'),
    path('dataadmin-menu/', views.dataAdminMenu, name='dataAdminMenu'),
    path('view-form/', views.view_form, name='view_form'),
    path('checking-page/', views.checking_page, name='checking_page'),
    path('checking-detail/', views.checking_detail, name='checking_detail'),
    path('submit-checking/', views.submit_checking, name='submit_checking'),
    path('fee-status/', views.fee_status, name='fee_status'),
    path('view-history/', views.view_history, name='view_history'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
