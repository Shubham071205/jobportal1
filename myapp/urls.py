from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),

    # ================= JOB SEEKER =================
    path('signup-jobseeker/', views.signup_jobseeker, name='signup_jobseeker'),
    path('login-jobseeker/', views.login_jobseeker, name='login_jobseeker'),
    path('jobseeker/dashboard/', views.jobseeker_dashboard, name='jobseeker_dashboard'),

    # ✅ ADD THESE
    path('jobseeker_search/', views.jobseeker_search, name='jobseeker_search'),
    path('jobseeker_applications/', views.jobseeker_applications, name='jobseeker_applications'),
    path('jobseeker_profile/', views.jobseeker_profile, name='jobseeker_profile'),

    # =================IDER =================
    path('signup-jobprovider/', views.signup_jobprovider, name='signup_jobprovider'),
    path('login-jobprovider/', views.login_jobprovider, name='login_jobprovider'),
    path('jobprovider-dashboard/', views.jobprovider_dashboard, name='jobprovider_dashboard'),

    # ================= LOGOUT =================
    path('logout/', views.logout_view, name='logout'),

    # ================= ADMIN =================
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),

    path('jobprovider/post-job/', views.jobprovider_post_job, name='jobprovider_post_job'),
    path('jobprovider/applications/', views.jobprovider_view_applications, name='jobprovider_view_applications'),
    path('company-profile/', views.jobprovider_company_profile, name='jobprovider_company_profile'),
    path('jobprovider/settings/', views.jobprovider_settings, name='jobprovider_settings'),
    path(
        "admin-report/",
        views.admin_generate_report,
        name="admin_generate_report"
    ),

    path(
        "job/<int:job_id>/",
        views.job_detail,
        name="job_detail"
    ),

    path(
        "apply/<int:job_id>/",
        views.apply_job,
        name="apply_job"
    ),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path(
        "update-application/<int:app_id>/",
        views.update_application_status,
        name="update_application_status"
    ),

]

