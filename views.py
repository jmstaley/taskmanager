from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from models import Task, Work, Project
from decorators import can_view_task, can_view_project
    
def index(request):
    user = request.user
    if user.is_authenticated():
        return redirect('taskmanager_dashboard')
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
    profile = request.user.get_profile()
    unassigned_tasks = Task.objects.unassigned_tasks(profile.org)
    projects = Project.objects.get_organisation_projects(profile.org)
    return render_to_response('taskmanager/dashboard.html',
                              {'user_tasks': user_tasks,
                               'unassigned_tasks': unassigned_tasks,
                               'projects': projects},
                              context_instance = RequestContext(request))

@login_required
@can_view_project
def project_detail(request, project_id=None):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.get_tasks_for_project(project_id)
    return render_to_response('taskmanager/project.html',
                              {'project': project,
                               'tasks': tasks},
                              context_instance = RequestContext(request))

@login_required
@can_view_task
def task_detail(request, task_id=None):
    task = get_object_or_404(Task, id=task_id)
    work = Work.objects.get_work_for_task(task)
    return render_to_response('taskmanager/task.html',
                              {'task': task,
                               'work': work},
                              context_instance = RequestContext(request))

