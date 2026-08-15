from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from website.models import UploadedFile


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:

            if User.objects.filter(username=username).exists():
                return render(
                    request,
                    'accounts/register.html',
                    {
                        'error': 'Username already exists. Please choose another username.'
                    }
                )

            user = User.objects.create_user(
                username=username,
                password=password
            )

            login(request, user)

            # Register ke baad Dashboard
            return redirect('dashboard')

    return render(request, 'accounts/register.html')


def user_login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            # Login ke baad Dashboard
            return redirect('dashboard')

        return render(
            request,
            'accounts/login.html',
            {
                'error': 'Invalid User ID or Password.'
            }
        )

    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):

    files = UploadedFile.objects.filter(
        owner=request.user
    ).order_by('-uploaded_at')

    return render(
        request,
        'website/dashboard.html',
        {
            'files': files
        }
    )