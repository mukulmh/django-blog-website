from django.shortcuts import render,redirect
from Auth.models import Account, ResetCode
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
import random
from django.core.mail import send_mail
from django.conf import settings



# Create your views here.


# login 
def login(request):

    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']

        user = auth.authenticate(phone=phone, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        
        else:
            messages.info(request, 'Invalid phone or password!')

    return render(request, 'auth/login.html')


# registration
def register(request):

    if request.method == 'POST':
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if Account.objects.filter(username=username).exists():
                messages.info(request,'Username is taken!')
            elif Account.objects.filter(email=email).exists():
                messages.info(request,'Email is taken!')
            elif Account.objects.filter(phone=phone).exists():
                messages.info(request,'Phone no is taken!')
            else:
                user = Account.objects.create_user(username=username,email=email,phone=phone,password=password1)
                user.save()
                messages.info(request,'User created! Now login.')
                return redirect('login')
        else:
            messages.info(request,'Password did not matched!')

        return redirect('register')

    return render(request,'auth/register.html')


# logout
def logout(request):
    auth.logout(request)
    messages.info(request, 'User logged out!')
    return redirect('login')


# reset password
def resetpassword(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        user = Account.objects.filter(phone=phone).first()
        if user is not None:
            request.session['phone'] = phone
            code = random.randint(0,999999)
            query = ResetCode.objects.filter(phone_id = phone).first()
            if query is not None:
                query.code = code
                query.save()
                
                subject = 'Password reset code'
                message = 'Your password reset code is {code}. If you are not expecting this email then please ignore.'.format(code=code)
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email,]
                send_mail(subject, message, from_email,recipient_list)
            else:
                query = ResetCode(code = code, phone_id = phone)
                query.save()
                
                subject = 'Password reset code'
                message = 'Your password reset code is {code}. If you are not expecting this email then please ignore.'.format(code=code)
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email,]
                send_mail(subject, message, from_email,recipient_list)
            return redirect('checkresetcode')
        messages.info(request, 'Phone no is not registered!')

    return render(request, 'auth/reset-password.html')


# reset password
def checkresetcode(request):
    if request.method == 'POST':
        code = request.POST['code']
        phone = request.session['phone']
        user = ResetCode.objects.filter(code=code, phone_id = phone).first()
        if user is not None:
            return redirect('confirmreset')
        messages.info(request, 'Invalid reset code!')
    return render(request, 'auth/check-reset-code.html')


# reset password
def confirmreset(request):
    phone = request.session['phone']
    user = Account.objects.get(phone=phone)
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            user.password = make_password(password1)
            user.save()
            messages.info(request,'Password reset successful. Now login with new password.')
            return redirect('login')
        messages.info(request, 'Password did not matched')
    return render(request, 'auth/confirm-reset.html')