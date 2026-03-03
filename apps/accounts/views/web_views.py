"""
Web authentication views for session-based login.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from apps.accounts.models import User
from apps.plans.models import Plan


@require_http_methods(["GET", "POST"])
def signup_view(request):
    """
    Handle user registration with username, email, and mobile number.
    Creates account directly without OTP verification.
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Validation
        if not email or not username or not password or not mobile_number:
            messages.error(request, 'All fields are required.')
            return render(request, 'auth/signup.html')

        # Basic mobile number validation (must be 10 digits)
        if not mobile_number.isdigit() or len(mobile_number) != 10:
            messages.error(request, 'Please enter a valid 10-digit Indian mobile number.')
            return render(request, 'auth/signup.html')

        # Format with +91 for Indian numbers
        formatted_mobile = f"+91{mobile_number}"

        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/signup.html')

        # Check if email already exists
        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'auth/signup.html')

        # Check if username already exists
        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'auth/signup.html')

        # Check if mobile number already exists
        if User.objects.filter(mobile_number=formatted_mobile).exists():
            messages.error(request, 'Mobile number already registered.')
            return render(request, 'auth/signup.html')

        try:
            # Get the Free plan (default)
            free_plan = Plan.objects.filter(name__iexact='Free').first()
            if not free_plan:
                free_plan = Plan.objects.create(name='Free', price=0)

            # Create the user directly
            user = User.objects.create_user(
                email=email,
                password=password,
                username=username,
                plan=free_plan,
                role='USER',
                mobile_number=formatted_mobile
            )

            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'auth/signup.html')

    return render(request, 'auth/signup.html')
