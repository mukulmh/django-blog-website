from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages


# Create your views here.


# login 
def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        
        else:
            messages.info(request, 'Invalid username or password!')

    return render(request, 'auth/login.html')


# registration
def register(request):

    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username is taken!')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email is taken!')
            else:
                user = User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name,password=password1)
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