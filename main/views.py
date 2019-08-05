from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    return render(request, 'base.html')


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
