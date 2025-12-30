from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # Job Seeker
    path("login-jobseeker/", views.login_jobseeker, name="login_jobseeker"),
    path("signup-jobseeker/", views.signup_jobseeker, name="signup_jobseeker"),
    path("jobseeker/dashboard/", views.jobseeker_dashboard, name="jobseeker_dashboard"),

    # Job Provider
    path("login-jobprovider/", views.login_jobprovider, name="login_jobprovider"),
    path("signup-jobprovider/", views.signup_jobprovider, name="signup_jobprovider"),
    path("jobprovider/dashboard/", views.jobprovider_dashboard, name="jobprovider_dashboard"),


    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-login/', views.admin_login, name='admin_login'),

    # Logout
    path("logout/", views.logout_view, name="logout"),
]

