from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Job Seeker
    path('signup-jobseeker/', views.signup_jobseeker, name='signup_jobseeker'),
    path('login-jobseeker/', views.login_jobseeker, name='login_jobseeker'),
    path('jobseeker/dashboard/', views.jobseeker_dashboard, name='jobseeker_dashboard'),

    # Job Provider
    path('signup-jobprovider/', views.signup_jobprovider, name='signup_jobprovider'),
    path('login-jobprovider/', views.login_jobprovider, name='login_jobprovider'),
    path('jobprovider/dashboard/', views.jobprovider_dashboard, name='jobprovider_dashboard'),

    # Logout
    path('logout/', views.logout_view, name='logout'),

    # Admin
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    # Debug/Test

]