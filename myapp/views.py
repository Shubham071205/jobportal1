from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import JobSeekerProfile, CompanyProfile


def home(request):
    return render(request, 'home.html')


# ================= JOB SEEKER =================

def signup_jobseeker(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not fullname or not email or not password:
            messages.error(request, "All fields required")
            return render(request, 'signup_jobseeker.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return render(request, 'signup_jobseeker.html')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=fullname
        )
        user.is_staff = False
        user.save()

        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect('jobseeker_dashboard')

    return render(request, 'signup_jobseeker.html')


def login_jobseeker(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user and not user.is_staff:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('jobseeker_dashboard')

        messages.error(request, "Invalid Job Seeker credentials")

    return render(request, 'login_jobseeker.html')


@login_required(login_url='login_jobseeker')
def jobseeker_dashboard(request):
    return render(request, 'dashboard_jobseeker.html')


@login_required(login_url='login_jobseeker')
def jobseeker_search(request):
    return render(request, 'jobseeker_search.html')


@login_required(login_url='login_jobseeker')
def jobseeker_applications(request):
    return render(request, 'jobseeker_applications.html')


@login_required(login_url='login_jobseeker')
def jobseeker_profile(request):
    profile, created = JobSeekerProfile.objects.get_or_create(user=request.user)

    edit_mode = request.GET.get('edit') == 'true'

    if request.method == "POST":
        request.user.first_name = request.POST.get('fullname')
        request.user.email = request.POST.get('email')

        profile.phone = request.POST.get('phone')
        profile.location = request.POST.get('location')
        profile.about_me = request.POST.get('about_me')
        profile.skills = request.POST.get('skills')

        request.user.save()
        profile.save()

        messages.success(request, "Profile updated successfully")
        return redirect('jobseeker_profile')

    skills_list = []
    if profile.skills:
        skills_list = [s.strip() for s in profile.skills.split(',') if s.strip()]

    return render(request, 'jobseeker_profile.html', {
        'profile': profile,
        'skills_list': skills_list,
        'edit_mode': edit_mode
    })


# ================= JOB PROVIDER =================

def signup_jobprovider(request):
    if request.method == 'POST':
        company_name = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not company_name or not email or not password:
            messages.error(request, "All fields required")
            return render(request, 'signup_jobprovider.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return render(request, 'signup_jobprovider.html')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=company_name
        )
        user.is_staff = True
        user.save()

        login(request, user)
        messages.success(request, "Job Provider account created successfully!")
        return redirect('jobprovider_dashboard')

    return render(request, 'signup_jobprovider.html')


def login_jobprovider(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user and user.is_staff:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('jobprovider_dashboard')

        messages.error(request, "Invalid Job Provider credentials")

    return render(request, 'login_jobprovider.html')


@login_required(login_url='login_jobprovider')
def jobprovider_dashboard(request):
    dummy_jobs = [
        {'title': 'Senior Python Developer', 'applicants': 12},
        {'title': 'Frontend React Developer', 'applicants': 8},
        {'title': 'DevOps Engineer', 'applicants': 5},
        {'title': 'Data Analyst', 'applicants': 15},
    ]

    return render(request, 'jobprovider_dashboard.html', {
        'jobs': dummy_jobs
    })


@login_required(login_url='login_jobprovider')
def jobprovider_post_job(request):
    return render(request, 'jobprovider_post_job.html')


@login_required(login_url='login_jobprovider')
def jobprovider_view_applications(request):
    return render(request, 'jobprovider_view_applications.html')


@login_required(login_url='login_jobprovider')
def jobprovider_company_profile(request):
    company, created = CompanyProfile.objects.get_or_create(
        user=request.user
    )

    edit_mode = request.GET.get('edit') == 'true'

    if request.method == 'POST':
        # ✅ Company name stored in USER
        request.user.first_name = request.POST.get('company_name')
        request.user.email = request.POST.get('email')
        request.user.save()

        # ✅ Company details stored in CompanyProfile
        company.about_company = request.POST.get('about_company')
        company.industry = request.POST.get('industry')
        company.company_size = request.POST.get('company_size')
        company.website = request.POST.get('website')
        company.location = request.POST.get('location')

        company.save()

        messages.success(request, "Company profile updated successfully")
        return redirect('jobprovider_company_profile')

    return render(request, 'jobprovider_company_profile.html', {
        'company': company,
        'edit_mode': edit_mode
    })


@login_required(login_url='login_jobprovider')
def jobprovider_settings(request):
    return render(request, 'jobprovider_settings.html')


# ================= LOGOUT =================

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')


# ================= SIMPLE ADMIN =================

def admin_login(request):
    if request.method == 'POST':
        if request.POST.get('username') == 'admin' and request.POST.get('password') == 'admin123':
            request.session['admin_logged_in'] = True
            request.session['admin_username'] = 'admin'
            return redirect('admin_dashboard')

        messages.error(request, "Invalid admin credentials")

    return render(request, 'admin_login.html')


def admin_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    return render(request, 'admin_dashboard.html', {
        'total_users': User.objects.count(),
        'total_job_seekers': User.objects.filter(is_staff=False).count(),
        'total_job_providers': User.objects.filter(is_staff=True).count(),
    })


def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')
