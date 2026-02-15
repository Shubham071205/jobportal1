from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import HttpResponse
import csv

from .models import Job, JobSeekerProfile, CompanyProfile, Application


# =====================================================
# BASIC PAGES
# =====================================================

def welcome(request):
    return render(request, "welcome.html")


def home(request):
    return render(request, "home.html")


# =====================================================
# JOB SEEKER
# =====================================================

def signup_jobseeker(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not fullname or not email or not password:
            messages.error(request, "All fields required")
            return render(request, "signup_jobseeker.html")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return render(request, "signup_jobseeker.html")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=fullname
        )

        login(request, user)
        return redirect("jobseeker_dashboard")

    return render(request, "signup_jobseeker.html")


def login_jobseeker(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user and not user.is_staff:
            login(request, user)
            return redirect("jobseeker_dashboard")

        messages.error(request, "Invalid credentials")

    return render(request, "login_jobseeker.html")


@login_required(login_url="login_jobseeker")
def jobseeker_dashboard(request):
    jobs = Job.objects.all().order_by("-created_at")

    applied_jobs = Application.objects.filter(
        seeker=request.user
    ).values_list("job_id", flat=True)

    context = {
        "recommended_jobs": jobs[:6],
        "applied_jobs": applied_jobs,
        "new_jobs_count": jobs.count(),
        "total_applications": len(applied_jobs),
    }

    return render(request, "dashboard_jobseeker.html", context)


@login_required(login_url="login_jobseeker")
def jobseeker_search(request):
    query = request.GET.get("q")
    jobs = Job.objects.all().order_by("-created_at")

    if query:
        jobs = jobs.filter(title__icontains=query)

    return render(request, "jobseeker_search.html", {
        "jobs": jobs,
        "query": query
    })


@login_required(login_url="login_jobseeker")
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    Application.objects.get_or_create(
        job=job,
        seeker=request.user,
        defaults={"status": "Pending"}
    )

    messages.success(request, "Application submitted!")

    return redirect("jobseeker_applications")


@login_required(login_url="login_jobseeker")
def jobseeker_applications(request):
    applications = Application.objects.filter(
        seeker=request.user
    ).select_related("job")

    return render(request, "jobseeker_applications.html", {
        "applications": applications
    })


@login_required(login_url="login_jobseeker")
def jobseeker_profile(request):
    profile, _ = JobSeekerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        request.user.first_name = request.POST.get("fullname")
        request.user.email = request.POST.get("email")

        profile.phone = request.POST.get("phone")
        profile.location = request.POST.get("location")
        profile.skills = request.POST.get("skills")
        profile.about_me = request.POST.get("about_me")

        request.user.save()
        profile.save()

        messages.success(request, "Profile updated")
        return redirect("jobseeker_profile")

    return render(request, "jobseeker_profile.html", {
        "profile": profile
    })


@login_required(login_url="login_jobseeker")
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    return render(request, "job_detail.html", {
        "job": job
    })


# =====================================================
# JOB PROVIDER
# =====================================================

def signup_jobprovider(request):
    if request.method == "POST":

        company = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "signup_jobprovider.html")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=company,
            is_staff=True
        )

        login(request, user)
        return redirect("jobprovider_dashboard")

    return render(request, "signup_jobprovider.html")


def login_jobprovider(request):
    if request.method == "POST":

        email = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect("jobprovider_dashboard")

        messages.error(request, "Invalid credentials")

    return render(request, "login_jobprovider.html")


@login_required(login_url="login_jobprovider")
def jobprovider_dashboard(request):
    jobs = Job.objects.filter(provider=request.user).order_by("-created_at")

    return render(request, "jobprovider_dashboard.html", {
        "jobs": jobs
    })


@login_required(login_url="login_jobprovider")
def jobprovider_post_job(request):
    if request.method == "POST":
        Job.objects.create(
            provider=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            location=request.POST.get("location"),
            salary=request.POST.get("salary"),
        )

        messages.success(request, "Job posted!")
        return redirect("jobprovider_dashboard")

    return render(request, "jobprovider_post_job.html")


@login_required(login_url="login_jobprovider")
def jobprovider_view_applications(request):
    applications = Application.objects.filter(
        job__provider=request.user
    ).select_related("job", "seeker")

    return render(request, "jobprovider_view_applications.html", {
        "applications": applications
    })


@require_POST
@login_required(login_url="login_jobprovider")
def update_application_status(request, app_id):
    application = get_object_or_404(
        Application,
        id=app_id,
        job__provider=request.user
    )

    status = request.POST.get("status")

    if status in ["Accepted", "Rejected"]:
        application.status = status
        application.save()

    return redirect("jobprovider_view_applications")


@login_required(login_url="login_jobprovider")
def jobprovider_company_profile(request):
    company, _ = CompanyProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        request.user.first_name = request.POST.get("company_name")
        request.user.email = request.POST.get("email")
        request.user.save()

        company.about_company = request.POST.get("about_company")
        company.industry = request.POST.get("industry")
        company.company_size = request.POST.get("company_size")
        company.website = request.POST.get("website")
        company.location = request.POST.get("location")

        company.save()

        messages.success(request, "Profile updated")
        return redirect("jobprovider_company_profile")

    return render(request, "jobprovider_company_profile.html", {
        "company": company
    })


# =====================================================
# ADMIN
# =====================================================

def admin_login(request):
    if request.method == "POST":

        if request.POST["username"] == "admin" and request.POST["password"] == "admin123":
            request.session["admin_logged_in"] = True
            return redirect("admin_dashboard")

        messages.error(request, "Invalid credentials")

    return render(request, "admin_login.html")


def admin_dashboard(request):
    if not request.session.get("admin_logged_in"):
        return redirect("admin_login")

    return render(request, "admin_dashboard.html", {
        "total_users": User.objects.count(),
        "job_seekers": User.objects.filter(is_staff=False).count(),
        "job_providers": User.objects.filter(is_staff=True).count(),
    })


def admin_generate_report(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=report.csv"

    writer = csv.writer(response)

    writer.writerow(["Username", "Email", "Type", "Active"])

    for user in User.objects.all():
        user_type = "Provider" if user.is_staff else "Seeker"

        writer.writerow([
            user.username,
            user.email,
            user_type,
            user.is_active
        ])

    return response


# =====================================================
# LOGOUT
# =====================================================

def logout_view(request):
    logout(request)
    return redirect("home")
def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')


@login_required(login_url='login_jobprovider')
def jobprovider_settings(request):
    return render(request, 'jobprovider_settings.html')
