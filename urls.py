from django.conf.urls.defaults import *

urlpatterns = patterns('taskmanager.views',
    url(r'^$', 'index', name='taskmanager_index'),
)
