from functools import wraps
from django.http import HttpResponseForbidden

from models import Task, Project

def can_view_task(view, task_id=None):
    @wraps(view)
    def inner(request, task_id=None):
        user_profile = request.user.get_profile()
        task = Task.objects.get(id=task_id)
        org = getattr(task, 'organisation', '')
        if not user_profile.org == org:
            return HttpResponseForbidden()
        else:
            return view(request, task_id=task_id)
    return inner

def can_view_project(view, project_id=None):
    @wraps(view)
    def inner(request, project_id=None):
        user_profile = request.user.get_profile()
        project = Project.objects.get(id=project_id)
        if not user_profile.org == project.organisation:
            return HttpResponseForbidden()
        else:
            return view(request, project_id=project_id)
    return inner

