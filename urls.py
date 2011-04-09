from django.conf.urls.defaults import *

urlpatterns = patterns('taskmanager.views',
    url(r'^$', 'index', name='taskmanager_index'),
    url(r'^detail/(?P<task_id>\d+)/$', 'task_detail', name='task_detail'),
    url(r'^dashboard/$', 'dashboard', name='taskmanager_dashboard'),
    url(r'^login/$', 'login_user', name='taskmanager_login'),
    url(r'^logout/$', 'logout_user', name='taskmanager_logout')
)
