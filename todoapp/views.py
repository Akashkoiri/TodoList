from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.views.generic.base import View
from .models import todo
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('NewTask')
        new_todo = todo(user=request.user, task=task)
        new_todo.save()

    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos
    }
    return render(request, 'todoapp/list.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 3:
            messages.error(request, 'Password must be at least 3 characters')
            return redirect('register')

        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'Error, username already exists, User another.')
            return redirect('register')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        messages.success(request, 'User successfully created, login now')
        return redirect('login')
    return render(request, 'todoapp/register.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = auth.authenticate(username=username, password=password)
        if validate_user is not None:
            auth.login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Error, wrong user details or user does not exist')
            return redirect('login')

    return render(request, 'todoapp/login.html', {})

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required
def deleteTask(request, id):
    get_todo = todo.objects.get(user=request.user, id=id)
    get_todo.delete()
    return redirect('home-page')

@login_required
def finishTask(request, id):
    get_todo = todo.objects.get(user=request.user, id=id)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')

class EditTask(View):
    def get(self, request, id):
        task = todo.objects.filter(id=id).first()
        context = {
            'todo': task
        }
        return render(request, 'todoapp/detail.html', context)

    def post(self, request, id):
        task = todo.objects.filter(id=id).first()

        task.task = str(request.POST.get('NewTask'))
        task.save()

        return redirect('/')