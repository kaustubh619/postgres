from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterUser
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import activation_token
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib import messages


@login_required(login_url='login')
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
    return redirect(home)


# def sign_up(request):
#     message = ''
#     if request.method == 'POST':
#         username = request.POST['username']
#         if User.objects.filter(username__iexact=username).exists():
#             pass
#             # return render(request, 'musicApp/sign_up_error.html')
#         email = request.POST['email']
#         password = request.POST['password']
#         user = User()
#         user.username = username
#         user.email = email
#         user.set_password(password)
#         user.save()
#         message = username + ' registered successfully !'
#     return render(request, 'registration.html', {'msg': message})


# def sign_up(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = 'Activate your account.'
#             message = render_to_string('acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
#                 'token': account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                         mail_subject, message, to=[to_email]
#             )
#             email.send()
#             return HttpResponse('Please confirm your email address to complete the registration')
#     else:
#         form = SignupForm()
#     return render(request, 'registration.html', {'form': form})


def sign_up(request):
    msg = ''
    form = RegisterUser(request.POST or None)
    if form.is_valid():
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already exist. Try with another email')
            msg = 'Email already exists. Try with another email'
            return render(request, 'registration.html', {'msg': msg})
        else:
            instance = form.save(commit=False)
            instance.is_active = False
            instance.save()
            site = get_current_site(request)
            mail_subject = "Confirmation mail for registration"
            message = render_to_string('acc_active_email.html', {
                "user": instance,
                'domain': site.domain,
                'uid': instance.id,
                'token': activation_token.make_token(instance)
            })
            to_email = form.cleaned_data.get('email')
            to_list = [to_email]
            from_email = settings.EMAIL_HOST_USER
            send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
            return render(request, 'econfirm_msg.html')
    return render(request, 'registration.html', {"form": form})


def activate(request, uid, token):
    try:
        user = get_object_or_404(User, pk=uid)
    except:
        raise Http404("No user found.")
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'after_confirmation_page.html')

