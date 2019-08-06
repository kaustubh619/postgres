from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    return render(request, 'home.html')


def login_user(request):
    if request.user.username:
        return redirect(home)
    message = ''
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        username = User.objects.get(email=email.lower()).username
        user = authenticate(username=username, password=password)
        if user is None:
            message = 'Invalid log in details!'
        else:
            login(request, user)
            return redirect(home)
    return render(request, 'login.html', {'msg': message})


def log_out(request):
    logout(request)
    return redirect(login_user)


def sign_up(request):
    message = ''
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username__iexact=username).exists():
            pass
            # return render(request, 'musicApp/sign_up_error.html')
        email = request.POST['email']
        password = request.POST['password']
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        user.save()
        message = username + ' registered successfully !'
    return render(request, 'registration.html', {'msg': message})

