from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),

    # ================= JOB SEEKER =================
    path('signup-jobseeker/', views.signup_jobseeker, name='signup-jobseeker'),
    path('login-jobseeker/', views.login_jobseeker, name='login_jobseeker'),
    path(
        'dashboard_jobseeker/',
        views.dashboard_jobseeker,
        name='jobseeker_dashborad'
    ),

    # ✅ ADD THESE
    path('jobseeker_search/', views.jobseeker_search, name='jobseeker_search'),
    path('jobseeker_applications/', views.jobseeker_applications, name='jobseeker_applications'),
    path('jobseeker_profile/', views.jobseeker_profile, name='jobseeker_profile'),

    # =================IDER =================
    path('signup-jobprovider/', views.signup_jobprovider, name='signup_jobprovider'),
    path('login-jobprovider/', views.login_jobprovider, name='login_jobprovider'),
    path('jobseeker/dashboard/', views.dashboard_jobseeker, name='dashboard_jobseeker'),

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
    # ================= JOB PROVIDER =================
    path('signup-jobprovider/', views.signup_jobprovider, name='signup_jobprovider'),
    path('login-jobprovider/', views.login_jobprovider, name='login_jobprovider'),

    path(
        'dashboard_jobprovider/',
        views.jobprovider_dashboard,
        name='jobprovider_dashboard'
    ),

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

    path(
        "update-application/<int:app_id>/",
        views.update_application_status,
        name="update_application_status"
    ),

    path("admin/users/", views.admin_view_users, name="admin_view_users"),
    path("admin/jobs/", views.admin_manage_jobs, name="admin_manage_jobs"),
    path("admin/jobs/delete/<int:job_id>/", views.admin_delete_job, name="admin_delete_job"),

    path("reports/jobs/", views.job_report, name="job_report"),
    path("admin-reports/", views.admin_reports_menu, name="admin_reports_menu"),

    path("reports/job-seekers/", views.job_seeker_report, name="job_seeker_report"),
    path("reports/job-providers/", views.job_provider_report, name="job_provider_report"),
    path("reports/jobs/", views.job_report, name="job_report"),
    path("reports/download/jobseekers/", views.download_job_seekers, name="download_job_seekers"),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

    path("reports/download/providers/", views.download_job_providers, name="download_job_providers"),

    path("reports/download/jobs/", views.download_jobs, name="download_jobs"),

    path('admin/view-users/', views.admin_view_users, name='admin_view_users'),
    path('admin/manage-jobs/', views.admin_manage_jobs, name='admin_manage_jobs'),

]

