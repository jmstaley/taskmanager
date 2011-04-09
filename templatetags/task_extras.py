from django import template

def show_tasks(tasks):
    return {'tasks': tasks}

register = template.Library()
register.inclusion_tag('taskmanager/task_table.html')(show_tasks)
