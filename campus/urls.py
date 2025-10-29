from django.urls import path
from . import views

app_name = 'campus'

urlpatterns = [
    path('', views.home, name='home'),

    # Zones
    path('zones/', views.zone_list_create, name='zone_list'),
    path('zones/<int:pk>/edit/', views.zone_edit, name='zone_edit'),
    path('zones/<int:pk>/delete/', views.zone_delete, name='zone_delete'),

    # Buildings
    path('buildings/', views.building_list_create, name='building_list'),
    path('buildings/<int:pk>/edit/', views.building_edit, name='building_edit'),
    path('buildings/<int:pk>/delete/', views.building_delete, name='building_delete'),

    # Divisions
    path('divisions/', views.division_list_create, name='division_list'),
    path('divisions/<int:pk>/edit/', views.division_edit, name='division_edit'),
    path('divisions/<int:pk>/delete/', views.division_delete, name='division_delete'),

]
