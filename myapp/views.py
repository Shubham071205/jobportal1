from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# ===========================
# HOME PAGE
# ===========================
def home(request):
    return render(request, 'home.html')


# ===========================
# JOB SEEKER SIGNUP
# ===========================
def signup_jobseeker(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        username = request.POST.get('username', '').strip() or email.split('@')[0]

        if not fullname or not email or not password:
            messages.error(request, "Please fill all fields.")
            return render(request, 'signup_jobseeker.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'signup_jobseeker.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'signup_jobseeker.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=fullname
        )
        user.save()

        login(request, user)
        return redirect('jobseeker_dashboard')

    return render(request, 'signup_jobseeker.html')


# ===========================
# JOB SEEKER LOGIN
# ===========================
def login_jobseeker(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Accept email or username
        if '@' in username_or_email:
            try:
                u = User.objects.get(email=username_or_email)
                username = u.username
            except User.DoesNotExist:
                username = None
        else:
            username = username_or_email

        user = None
        if username:
            user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('jobseeker_dashboard')

        messages.error(request, "Invalid credentials.")

    return render(request, 'login_jobseeker.html')


# ===========================
# JOB SEEKER DASHBOARD
# ===========================
@login_required(login_url='login_jobseeker')
def jobseeker_dashboard(request):

    context = {
        "user": request.user,
        "recommended_jobs": [
            {"title": "Software Developer", "company": "Google", "location": "Bengaluru"},
            {"title": "Frontend Developer", "company": "TCS", "location": "Mumbai"},
        ],
        "recent_applications": [
            {"title": "Python Developer", "company": "Infosys", "status": "Under Review"},
            {"title": "Django Developer", "company": "Wipro", "status": "Shortlisted"},
        ],
    }

    return render(request, 'dashboard_jobseeker.html', context)


# ================================================================
# JOB PROVIDER MODULE
# ================================================================

# -----------------------------
# JOB PROVIDER SIGNUP
# -----------------------------
def signup_jobprovider(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        username = email.split('@')[0]

        if not fullname or not email or not password:
            messages.error(request, "All fields required.")
            return render(request, 'signup_jobprovider.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'signup_jobprovider.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=fullname
        )
        user.save()

        login(request, user)
        return redirect('jobprovider_dashboard')

    return render(request, 'signup_jobprovider.html')


# -----------------------------
# JOB PROVIDER LOGIN
# -----------------------------
def login_jobprovider(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Invalid Email or Password")
            return render(request, 'login_jobprovider.html')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('jobprovider_dashboard')

        messages.error(request, "Invalid Email or Password")

    return render(request, 'login_jobprovider.html')


# -----------------------------
# JOB PROVIDER DASHBOARD
# -----------------------------
@login_required(login_url='login_jobprovider')
def jobprovider_dashboard(request):

    sample_jobs = [
        {"title": "Python Developer", "applicants": 12},
        {"title": "UI/UX Designer", "applicants": 8},
    ]

    return render(request, 'dashboard_jobprovider.html', {"jobs": sample_jobs})


# -----------------------------
# LOGOUT
# -----------------------------
def logout_view(request):
    logout(request)
    return redirect('home')
def signup_jobprovider(request):
    return render(request, 'signup_jobprovider.html')

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib import messages

# ================= ADMIN LOGIN (HARDCODED) =================
def admin_login(request):
    # default admin credentials
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin123"

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            # store admin session
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid Admin Username or Password")

    return render(request, 'admin_login.html')


# ================= ADMIN DASHBOARD =================
def admin_dashboard(request):
    # protect dashboard
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    return render(request, 'admin_dashboard.html')


# ================= ADMIN LOGOUT =================
def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')
