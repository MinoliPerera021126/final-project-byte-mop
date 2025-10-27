from django.shortcuts import redirect
from functools import wraps


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'admin':
            return view_func(request, *args, **kwargs)
        return redirect('ma_dashboard')
    return wrapper


def ma_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'ma':
            return view_func(request, *args, **kwargs)
        return redirect('admin_dashboard')
    return wrapper
