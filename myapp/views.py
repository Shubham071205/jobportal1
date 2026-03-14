from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import HttpResponse
import csv
from .models import CompanyProfile
from .models import JobSeekerProfile
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


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def signup_jobseeker(request):
    if request.method == "POST":
        username = request.POST.get("username")
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup-jobseeker")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = fullname
        user.save()

        return redirect("login-jobseeker")

    return render(request, "signup_jobseeker.html")

def login_jobseeker(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user and not user.is_staff:
            login(request, user)
            return redirect("dashboard_jobseeker")

        messages.error(request, "Invalid credentials")

    return render(request, "login_jobseeker.html")


from django.utils.timezone import now
from django.db.models import Count

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Job, Application


@login_required(login_url='login_jobseeker')
def dashboard_jobseeker(request):
    # All jobs posted by providers
    recommended_jobs = Job.objects.all().order_by('-created_at')[:10]

    # Applications of current user
    applications = Application.objects.filter(seeker=request.user)

    # IDs of applied jobs (for button state)
    applied_jobs = applications.values_list('job_id', flat=True)

    # counts
    total_applications = applications.count()
    shortlisted_count = applications.filter(status="Accepted").count()

    # recent jobs (last 7 days)
    from django.utils import timezone
    from datetime import timedelta

    week_ago = timezone.now() - timedelta(days=7)
    new_jobs_count = Job.objects.filter(created_at__gte=week_ago).count()

    # recent applications
    recent_applications = applications.order_by('-applied_at')[:5]

    context = {
        "recommended_jobs": recommended_jobs,
        "applied_jobs": applied_jobs,
        "recent_applications": recent_applications,
        "total_applications": total_applications,
        "shortlisted_count": shortlisted_count,
        "new_jobs_count": new_jobs_count,
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


@login_required(login_url='login_jobseeker')
def jobseeker_applications(request):
    apps = Application.objects.filter(seeker=request.user)

    return render(
        request,
        "jobseeker_applications.html",
        {"applications": apps}
    )


@login_required(login_url='login_jobseeker')
def jobseeker_profile(request):
    profile, created = JobSeekerProfile.objects.get_or_create(
        user=request.user
    )

    # ✅ Detect edit mode
    edit_mode = request.GET.get("edit") == "true"

    if request.method == "POST":

        request.user.first_name = request.POST.get("fullname")
        request.user.email = request.POST.get("email")
        request.user.save()

        profile.phone = request.POST.get("phone")
        profile.location = request.POST.get("location")
        profile.skills = request.POST.get("skills")
        profile.about_me = request.POST.get("about_me")

        profile.save()

        messages.success(request, "Profile updated!")

        # ✅ Return to normal view
        return redirect("jobseeker_profile")

    # split skills for display
    skills_list = []
    if profile.skills:
        skills_list = [s.strip() for s in profile.skills.split(",")]

    return render(request, "jobseeker_profile.html", {
        "profile": profile,
        "skills_list": skills_list,
        "edit_mode": edit_mode
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

        CompanyProfile.objects.create(user=user)
        login(request, user)
        return redirect("jobprovider_dashboard")

    return render(request, "signup_jobseeker.html")


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
@login_required(login_url="login_jobprovider")
def jobprovider_post_job(request):
    if request.method == "POST":
        salary = request.POST.get("salary").replace(",", "")
        salary = int(salary)

        Job.objects.create(
            provider=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            location=request.POST.get("location"),
            salary=salary,
        )

        messages.success(request, "Job posted!")
        return redirect("jobprovider_dashboard")

    return render(request, "jobprovider_post_job.html")


@login_required(login_url='login_jobprovider')
def jobprovider_view_applications(request):

    applications = Application.objects.filter(
        job__provider=request.user
    )

    return render(
        request,
        "jobprovider_view_applications.html",
        {"applications": applications}
    )



@require_POST
@login_required(login_url='login_jobprovider')
def update_application_status(request, app_id):

    application = get_object_or_404(
        Application,
        id=app_id,
        job__provider=request.user
    )

    if request.method == "POST":

        status = request.POST.get("status")

        if status in ["Accepted", "Rejected"]:
            application.status = status
            application.save()

    return redirect("jobprovider_view_applications")


@login_required(login_url='login_jobprovider')
def jobprovider_company_profile(request):
    company, created = CompanyProfile.objects.get_or_create(
        user=request.user
    )

    # ✅ Detect edit mode from URL
    edit_mode = request.GET.get("edit") == "true"

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

        messages.success(request, "Profile updated!")

        # ✅ Redirect back to normal view
        return redirect("jobprovider_company_profile")

    return render(request, "jobprovider_company_profile.html", {
        "company": company,
        "edit_mode": edit_mode
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


from django.contrib.auth.models import User
from .models import Job, JobSeekerProfile, CompanyProfile

def admin_dashboard(request):
    if not request.session.get("admin_logged_in"):
        return redirect("admin_login")

    total_users = User.objects.filter(is_superuser=False).count()
    total_job_seekers = User.objects.filter(is_staff=False, is_superuser=False).count()
    total_job_providers = User.objects.filter(is_staff=True, is_superuser=False).count()
    total_jobs = Job.objects.count()

    return render(request, "admin_dashboard.html", {
        "admin_username": "Admin",
        "total_users": total_users,
        "total_job_seekers": total_job_seekers,
        "total_job_providers": total_job_providers,
        "total_jobs": total_jobs,
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


from django.contrib.auth.models import User
from django.shortcuts import render
from .models import JobSeekerProfile, CompanyProfile


def admin_view_users(request):
    users = User.objects.all().order_by("-date_joined")

    user_data = []

    for u in users:

        role = "User"

        seeker = JobSeekerProfile.objects.filter(user=u).first()
        provider = CompanyProfile.objects.filter(user=u).first()

        if seeker:
            role = "Job Seeker"

        if provider:
            role = "Job Provider"

        user_data.append({
            "user": u,
            "role": role,
            "seeker": seeker,
            "provider": provider,
        })

    return render(request, "admin_view_users.html", {
        "user_data": user_data
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import Job


def admin_manage_jobs(request):
    jobs = Job.objects.select_related("provider").all()

    return render(request, "admin_manage_jobs.html", {
        "jobs": jobs
    })


def admin_delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.delete()

    return redirect("admin_manage_jobs")


from django.shortcuts import render


def admin_reports_menu(request):
    return render(request, "admin_reports_menu.html")


from django.contrib.auth.models import User
from django.shortcuts import render

def job_seeker_report(request):
    seekers = User.objects.filter(
        is_staff=False,
        is_superuser=False
    )

    return render(request, "job_seeker_report.html", {
        "seekers": seekers
    })


def job_provider_report(request):
    providers = User.objects.filter(company_profile__isnull=False)
    return render(request, "job_provider_report.html", {"providers": providers})


def job_report(request):
    jobs = Job.objects.all()
    return render(request, "job_report.html", {"jobs": jobs})


def admin_reports_menu(request):
    return render(request, "admin_reports_menu.html")


import csv
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import JobSeekerProfile


def download_job_seekers(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="job_seekers_report.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID", "Name", "Email", "Phone", "Location", "Skills"])

    seekers = User.objects.filter(seeker_profile__isnull=False)

    for s in seekers:
        profile = s.seeker_profile
        writer.writerow([
            s.id,
            s.username,
            s.email,
            profile.phone,
            profile.location,
            profile.skills
        ])

    return response


from .models import CompanyProfile


def download_job_providers(request):
    import csv
    from django.http import HttpResponse
    from django.contrib.auth.models import User

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="job_providers_report.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID", "Company/User", "Email", "Industry", "Location", "Website"])

    providers = User.objects.filter(company_profile__isnull=False)

    for p in providers:
        profile = p.company_profile

        writer.writerow([
            p.id,
            p.username,
            p.email,
            profile.industry,
            profile.location,
            profile.website
        ])

    return response


from .models import Job


def download_jobs(request):
    import csv
    from django.http import HttpResponse

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="jobs_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Job ID",
        "Title",
        "Provider",
        "Location",
        "Salary",
        "Applicants",
        "Created"
    ])

    jobs = Job.objects.all()

    for job in jobs:
        writer.writerow([
            job.id,
            job.title,
            job.provider.username,
            job.location,
            job.salary,
            job.applicants,
            job.created_at
        ])

    return response


from django.db.models import Sum
from .models import Job


def jobprovider_dashboard(request):
    jobs = Job.objects.filter(provider=request.user)

    # REAL total applicants calculation
    total_applicants = jobs.aggregate(total=Sum('applicants'))['total'] or 0

    context = {
        'jobs': jobs,
        'total_applicants': total_applicants,
    }

    return render(request, 'jobprovider_dashboard.html', context)


from django.shortcuts import render
from .models import Job

from django.shortcuts import render
from .models import Job


def jobseeker_search(request):
    jobs = Job.objects.all()

    query = request.GET.get('q')
    location = request.GET.get('location')
    salary = request.GET.get('salary')
    job_type = request.GET.get('job_type')

    if query:
        jobs = jobs.filter(title__icontains=query)

    if location:
        jobs = jobs.filter(location__icontains=location)

    if salary:
        jobs = jobs.filter(salary__gte=salary)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    context = {
        "jobs": jobs
    }

    return render(request, "jobseeker_search.html", context)


from django.shortcuts import redirect
from .models import JobSeekerProfile

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User

def delete_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        user.delete()
    return redirect('/reports/job-seekers/')


from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User


def delete_provider(request, provider_id):
    if request.method == "POST":
        provider = get_object_or_404(User, id=provider_id)
        provider.delete()

    return redirect('job_provider_report')
