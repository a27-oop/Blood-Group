from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('login/', views.login_view, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('logout/', views.logout_view, name='logout'),

    path('find-donor/', views.donor_search, name='find_donor'),

    path(
    'emergency-request/',
    views.emergency_request,
    name='emergency_request'),

    path(
    'health-tips/',
    views.health_tips,
    name='health_tips'),
    


]