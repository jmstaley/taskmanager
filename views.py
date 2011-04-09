from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from models import Task, Work
    
def index(request):
    return render_to_response('taskmanager/index.html',
                              context_instance = RequestContext(request))

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('taskmanager_dashboard')

    messages.add_message(request, messages.ERROR, 'Invalid username/password')
    return redirect('taskmanager_index')

def logout_user(request):
    logout(request)
    return redirect('taskmanager_index')

@login_required
def dashboard(request):
    user_tasks = Task.objects.get_tasks_for_user(request.user)
    unassigned_tasks = Task.objects.unassigned_tasks()
    return render_to_response('taskmanager/dashboard.html',
                              {'user_tasks': user_tasks,
                               'unassigned_tasks': unassigned_tasks},
                              context_instance = RequestContext(request))

@login_required
def task_detail(request, task_id=None):
    task = Task.objects.get(id=task_id)
    work = Work.objects.get_work_for_task(task)
    return render_to_response('taskmanager/task.html',
                              {'task': task,
                               'work': work},
                              context_instance = RequestContext(request))
