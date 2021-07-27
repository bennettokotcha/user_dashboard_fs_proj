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
        }
        return render(request, 'all_users.html', context) 
    else:
        context = {
            'all_users': User.objects.all(),
        }
        return render(request, 'manage_user.html', context)

def user_edit_page(request, id):
    if request.session['user_id'] == id:
        context = {
            'user': User.objects.get(id=id)
        } 
        return render(request, 'edit_profile.html', context)
    return redirect('/dashboard/admin')

def admin_edit_page(request, id):
    user1 = User.objects.get(id=id)
    print(user1.user_level, user1.first_name)
    users = User.objects.all()    
    if request.session['user_id'] == id or user1.user_level is True:
        context = {
            'admin': User.objects.get(id=id)
        }
        return render(request, 'edit_user.html', context)
    return redirect('/dashboard/admin')

def posts_page(request, id):
    show_user = User.objects.get(id=id)
    context = {
        'show_user' : User.objects.get(id=id)
    }
    return render(request, 'posts.html', context)

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

            user = User.objects.create(
                first_name=request.POST['first_name'], 
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                user_level=False,
                password=pw_hash,
                confirm_pw=request.POST['confirm_pw']
                )
            request.session['user_id'] = user.id
            request.session['user_name']= user.first_name
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

def add_user_proccess(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        user = User.objects.filter(email = request.POST['email'])
        if user:
            messages.error(request, 'Email already exist, please register with a different email address!')
            return redirect('/user/new')
        if len(errors) > 0 :
            for k, v in errors.items():
                messages.error(request, v)#extra_tags=key
            return redirect('/user/new')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            print(pw_hash)
    
    added_user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        user_level=True,
        password=pw_hash,
        confirm_pw=request.POST['confirm_pw']
    )
    return redirect('/dashboard/admin')

def edit_info_proccess(request, id):
    if request.method == 'POST':
        this_user = User.objects.get(id=id)
        errors = User.objects.info_edit_validator(request.POST)
        if not request.POST['email'] == this_user.email:
            user = User.objects.filter(email = request.POST['email'])
            if user:
                messages.error(request, 'Email already exist, please register with a different email address!')
                return redirect(f'/users/edit/{id}')
        if len(errors) > 0 :
            for k, v in errors.items():
                messages.error(request, v)#extra_tags=key
            return redirect(f'/users/edit/{id}')
        this_user = User.objects.get(id=id)
        this_user.first_name = request.POST['first_name']
        this_user.last_name = request.POST['last_name']
        this_user.email = request.POST['email']
        this_user.save()
        return redirect('/dashboard/admin')
    return redirect('/')

def edit_password_proccess(request, id):
    if request.method == 'POST':
        this_user = User.objects.get(id=id)
        errors = User.objects.password_edit_validator(request.POST)
        if len(errors) > 0 :
            for k, v in errors.items():
                messages.error(request, v)#extra_tags=key
            return redirect(f'/users/edit/{id}')

        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        this_user.password = pw_hash
        this_user.confirm_pw = request.POST['confirm_pw']
        this_user.save()
        return redirect('/dashboard/admin')
    return redirect('/')

def edit_desc_proccess(request, id):
    if request.method == 'POST':
        this_user = User.objects.get(id=id)
        this_user.desc = request.POST['desc']
        this_user.save()
        return redirect('/dashboard/admin')

def edit_userinfo_proccess(request, id):
    this_user = User.objects.get(id=id)
    this_user.first_name =  request.POST['first_name']
    this_user.last_name = request.POST['last_name']
    this_user.user_level = request.POST['user_level']
    this_user.email = request.POST['email']
    this_user.save()
    return redirect('/dashboard/admin')


def remove_user(request, number):
    if request.method=='GET':
        user = User.objects.get(id=number)
        user.delete()
        return redirect('/dashboard/admin')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')
# Create your views here.
