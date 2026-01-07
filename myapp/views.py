from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
    return render(request, 'jobseeker_profile.html')

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

        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('jobprovider_dashboard')
        else:
            messages.error(request, "Invalid Job Provider credentials")

    return render(request, 'login_jobprovider.html')


@login_required(login_url='login_jobprovider')
def jobprovider_dashboard(request):
    # Create dummy jobs for testing
    dummy_jobs = [
        {'title': 'Senior Python Developer', 'applicants': 12},
        {'title': 'Frontend React Developer', 'applicants': 8},
        {'title': 'DevOps Engineer', 'applicants': 5},
        {'title': 'Data Analyst', 'applicants': 15},
    ]

    context = {
        'jobs': dummy_jobs,
    }

    return render(request, 'jobprovider_dashboard.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')


# ================= SIMPLE ADMIN SYSTEM =================

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Simple hardcoded check
        if username == 'admin' and password == 'admin123':
            # Store admin status in session
            request.session['admin_logged_in'] = True
            request.session['admin_username'] = 'admin'
            messages.success(request, "Admin login successful!")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid admin credentials")

    return render(request, 'admin_login.html')


def admin_dashboard(request):
    # Check if admin is logged in via session
    if not request.session.get('admin_logged_in'):
        messages.error(request, "Please login first")
        return redirect('admin_login')

    # Get data for dashboard
    total_users = User.objects.count()
    total_job_seekers = User.objects.filter(is_staff=False).count()
    total_job_providers = User.objects.filter(is_staff=True).count()

    context = {
        'admin_username': request.session.get('admin_username', 'Admin'),
        'total_users': total_users,
        'total_job_seekers': total_job_seekers,
        'total_job_providers': total_job_providers,
    }

    return render(request, 'admin_dashboard.html', context)


def admin_logout(request):
    # Clear admin session
    request.session.flush()
    messages.success(request, "Admin logged out successfully!")
    return redirect('admin_login')