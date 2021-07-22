from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'dash_home.html')

def register_page(request):
    return render(request, 'register.html')

def login_page(request):
    return render(request, 'login.html')

def add_user_page(request):
    return render(request, 'add_user.html')

def user_admin_page(request):
    user = User.objects.get(id=request.session['user_id'])
    if user.user_level is True: 
        context = {
            'all_users': User.objects.all(),
            # 'admin': User.objects.get(id=request.session['admin_id'])
        }
        return render(request, 'manage_user.html', context)
    else:

        return render(request, 'all_users.html')

def register_admin(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        user = User.objects.filter(email = request.POST['email'])
        if user:
            messages.error(request, 'Email already exist, please register with a different email address!')
            return redirect('/register')
        if len(errors) > 0 :
            for k, v in errors.items():
                messages.error(request, v)#extra_tags=key
            return redirect('/register')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            print(pw_hash)

            admin_user = User.objects.create(
                first_name=request.POST['first_name'], 
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                user_level=True,
                password=pw_hash,
                confirm_pw=request.POST['confirm_pw']
                )
            request.session['user_id'] = admin_user.id
            request.session['user_name']= admin_user.first_name
        return redirect('/dashboard/admin')

def login_proccess(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0 :
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/login')
    user = User.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]

        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_name'] = logged_user.first_name
            request.session['user_id'] = logged_user.id
            return redirect('/dashboard/admin')
        else:
            messages.error(request, 'Invalid email or password')
        return redirect('/login')
    messages.error(request, 'Invalid email or password')   
    return redirect('/login')

def logout(request):
    request.session.flush()
    return redirect('/')
# Create your views here.
