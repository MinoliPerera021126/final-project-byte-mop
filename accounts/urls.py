from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('ma-login/', views.ma_login_view, name='ma_login'),
    path('login/', views.login_redirect, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('ma-dashboard/', views.ma_dashboard, name='ma_dashboard'),

    path('create-ma/', views.create_ma_view, name='create_ma'),
    path('delete-ma/<int:user_id>/', views.delete_ma_view, name='delete_ma'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('profile/', views.view_profile, name='profile'),
]
urlpatterns += staticfiles_urlpatterns()
