from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from .forms import CreateMAForm
from .decorators import admin_required, ma_required


# ------------------------
# PUBLIC PAGES
# ------------------------

def home(request):
    return render(request, 'accounts/welcome.html', {
        'title': 'Welcome to Cleaning Management System',
        'description': (
            "A digital platform developed for the University of Sri Jayewardenepura to streamline "
            "cleaning operations, task scheduling, and administrative coordination for a smarter campus."
        )
    })


def about(request):
    return render(request, 'accounts/about.html', {
        'title': 'About Us',
        'description': (
            "Learn more about how the Cleaning Management System supports efficient maintenance, "
            "management, and reporting across the University’s facilities."
        )
    })


def contact(request):
    return render(request, 'accounts/contact.html', {
        'title': 'Contact Us',
        'description': (
            "Need assistance or have inquiries about the system? Reach out to the IT or administrative team "
            "of the University of Sri Jayewardenepura."
        )
    })


# ------------------------
# SHARED LOGIN HANDLER
# ------------------------
def _process_login(request, expected_role=None):
    """Handles both Admin and MA logins with role verification."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not hasattr(user, 'profile'):
                messages.error(
                    request, "This account doesn't have a role assigned. Contact system admin.")
                return redirect('admin_login')

            if expected_role and user.profile.role != expected_role:
                messages.error(
                    request, f"This login page is only for {expected_role.upper()}s.")
                return redirect('admin_login' if expected_role == 'admin' else 'ma_login')

            login(request, user)
            if user.profile.role == 'admin':
                return redirect('admin_dashboard')
            elif user.profile.role == 'ma':
                return redirect('ma_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return None


# ------------------------
# LOGIN VIEWS
# ------------------------
def admin_login_view(request):
    response = _process_login(request, expected_role='admin')
    if response:
        return response
    return render(request, 'accounts/admin_login.html', {
        'title': 'System Admin Login',
        'description': (
            "Access the administrative panel to manage users, assign tasks, and oversee cleaning operations "
            "within the University of Sri Jayewardenepura."
        )
    })


def ma_login_view(request):
    response = _process_login(request, expected_role='ma')
    if response:
        return response
    return render(request, 'accounts/ma_login.html', {
        'title': 'Management Assistant Login',
        'description': (
            "Log in to manage daily cleaning schedules, submit reports, and monitor assigned zones "
            "as part of the university’s facility management process."
        )
    })


def login_redirect(request):
    """Redirects /accounts/login/ → admin login by default"""
    return redirect('admin_login')


# ------------------------
# LOGOUT VIEW
# ------------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('admin_login')


# ------------------------
# ADMIN DASHBOARD + FUNCTIONS
# ------------------------
@login_required
@admin_required
def admin_dashboard(request):
    ma_users = Profile.objects.filter(role='ma')
    ma_count = ma_users.count()
    context = {
        'title': 'Admin Dashboard',
        'description': (
            "System Administrator Panel — manage Management Assistant accounts, monitor cleaning data, "
            "and ensure all operational records remain up to date across departments."
        ),
        'ma_users': ma_users,
        'ma_count': ma_count
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
@admin_required
def create_ma_view(request):
    """System Admin creates a new Management Assistant"""
    if request.method == 'POST':
        form = CreateMAForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']

            # --- VALIDATION RULES ---
            if " " in username:
                messages.error(request, 'Username cannot contain spaces.')
                return redirect('create_ma')

            if len(password) < 8:
                messages.error(
                    request, 'Password must be at least 8 characters long.')
                return redirect('create_ma')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
                return redirect('create_ma')

            # --- CREATE USER ---
            user = User.objects.create_user(
                username=username, email=email, password=password)
            Profile.objects.create(user=user, role='ma', phone=phone)
            messages.success(
                request, f'Management Assistant "{username}" created successfully.')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid form data.')
    else:
        form = CreateMAForm()

    return render(request, 'accounts/create_ma.html', {
        'form': form,
        'title': 'Create Management Assistant',
        'description': (
            "Add new Management Assistant accounts to the system and assign them responsibilities "
            "for cleaning and maintenance record handling."
        )
    })


@login_required
@admin_required
def delete_ma_view(request, user_id):
    """System Admin deletes a Management Assistant"""
    try:
        user = User.objects.get(id=user_id)
        if user == request.user:
            messages.error(
                request, "You cannot delete your own admin account.")
            return redirect('admin_dashboard')

        if hasattr(user, 'profile') and user.profile.role == 'ma':
            user.delete()
            messages.success(
                request, f'Management Assistant \"{user.username}\" deleted successfully.')
        else:
            messages.error(
                request, 'You can only delete Management Assistant accounts.')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')

    return redirect('admin_dashboard')


@login_required
@admin_required
def change_ma_password_view(request, user_id):
    """Allows Admin to change a Management Assistant's password"""
    try:
        user = User.objects.get(id=user_id)
        if not hasattr(user, 'profile') or user.profile.role != 'ma':
            messages.error(request, 'You can only change passwords for MAs.')
            return redirect('admin_dashboard')

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if not new_password or not confirm_password:
                messages.error(request, 'Please fill in both password fields.')
                return redirect('change_ma_password', user_id=user_id)

            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('change_ma_password', user_id=user_id)

            if len(new_password) < 8:
                messages.error(
                    request, 'Password must be at least 8 characters long.')
                return redirect('change_ma_password', user_id=user_id)

            user.set_password(new_password)
            user.save()
            messages.success(
                request, f'Password for "{user.username}" changed successfully.')
            return redirect('admin_dashboard')

    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('admin_dashboard')

    return render(request, 'accounts/change_ma_password.html', {
        'user': user,
        'title': 'Change MA Password',
        'description': 'Update the password for a Management Assistant securely.',
    })


# ------------------------
# MANAGEMENT ASSISTANT DASHBOARD
# ------------------------
@login_required
@ma_required
def ma_dashboard(request):
    """Dashboard for Management Assistants (admins cannot open this)"""
    profile = request.user.profile
    return render(request, 'accounts/ma_dashboard.html', {
        'profile': profile,
        'title': 'MA Dashboard',
        'description': (
            "Management Assistant Panel — view assigned schedules, record cleaning activities, "
            "and maintain transparent communication with the administrative team."
        )
    })


# ------------------------
# USER PROFILE (for both roles)
# ------------------------
@login_required
def view_profile(request):
    """Displays profile info for both Admin and MA"""
    profile = request.user.profile
    return render(request, 'accounts/profile.html', {
        'title': 'User Profile',
        'user': request.user,
        'profile': profile,
        'description': (
            "View and manage your personal information, including contact details and system role, "
            "within the Cleaning Management System."
        )
    })
