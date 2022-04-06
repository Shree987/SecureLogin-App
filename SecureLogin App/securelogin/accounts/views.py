import datetime
from .forms import UserCreationForm
from accounts.models import MyUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def home(request):
    return render(request,'accounts/home.html')


@login_required
def index(request):
    return render(request,'accounts/index.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect("accounts:home")


def sign_up(request):
    if request.user.is_authenticated:
        logout(request)
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.login_attempts = 0
            form.blocked_time = datetime.datetime.now()
            form.password_expiry = datetime.datetime.now() + datetime.timedelta(minutes=10)
            user = form.save()
            login(request,user)
            return redirect('accounts:index')
    context['form']=form
    return render(request,'registration/sign_up.html',context)


def user_login(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        current_time = datetime.datetime.now()
        if user:
            if user.blocked_time.timestamp() < current_time.timestamp():
                user.login_attempts = 0
            if user.login_attempts == 5:
                user.blocked_time = current_time +  datetime.timedelta(minutes=5)
            if user.login_attempts >= 5 and user.blocked_time.timestamp() >= current_time.timestamp():
                # User has been temporarily blocked from service
                return render(request, 'registration/login.html',
                              {'error_message': "You have exceeded maximum the number of attempts."
                                                "Please wait for few hours before attempting again!"})
            if user.password_expiry.timestamp() <= current_time.timestamp():
                # User's password has expired
                messages.success(request, "Your password has expired. "
                                                "Kindly reset your password to access your account again!")
                return redirect("password_reset")
            user.login_attempts = 0
            user.blocked_time = current_time
            user.password_expiry = current_time + datetime.timedelta(minutes=10)
            user.save()
            login(request, user)
            return redirect("accounts:index")
        else:
            try:
                user = MyUser.objects.get(username=username)
            except:
                # No user with that Username exists
                return render(request, 'registration/login.html',
                              {'error_message': "Invalid login details provided.\nLogin failed."})
            else:
                # User provided wrong password
                user.login_attempts += 1
                user.save()
                if user.login_attempts == 5:
                    user.blocked_time = current_time +  datetime.timedelta(minutes=5)
                    user.save()
                if user.login_attempts >= 5 and user.blocked_time.timestamp() >= current_time.timestamp():
                    return render(request, 'registration/login.html',
                                  {'error_message': "You have exceeded maximum the number of attempts. "
                                                    "Please wait for few hours before attempting again!"})
                else:
                    message = "You have made " + str(user.login_attempts) + \
                              " number of unsuccessful attempts. After " + str(5 - user.login_attempts) + \
                              " more wrong attempts, your account will be temporarily deactivated."
                    return render(request, 'registration/login.html', {"error_message": message})
    else:
        return render(request, 'registration/login.html', {'error_message': None})


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = MyUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password/password_reset.html",
                  context={"password_reset_form":password_reset_form})