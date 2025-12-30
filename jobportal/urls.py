from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('home/', views.home, name='home_page'),

    # Job Seeker
    path('login-jobseeker/', views.login_jobseeker, name='login_jobseeker'),
    path('signup-jobseeker/', views.signup_jobseeker, name='signup_jobseeker'),
    path('jobseeker/dashboard/', views.jobseeker_dashboard, name='jobseeker_dashboard'),

    # Job Provider
    path('login-jobprovider/', views.login_jobprovider, name='login_jobprovider'),
    path('signup-jobprovider/', views.signup_jobprovider, name='signup_jobprovider'),

    # Admin Dashboard ✅
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),

    # Logout
    path('logout/', views.logout_view, name='logout'),
]
