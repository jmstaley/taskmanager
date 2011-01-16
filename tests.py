"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from taskmanager.models import Project, Task

from datetime import date

class ProjectTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(description='this is a test project',
                                              due_date=date(2001, 12, 30),
                                              name='test project')

class TaskTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(description='this is a test project',
                                              due_date=date(2002, 12, 30),
                                              name='test project')

        self.task = Task.objects.create(creation_date=date(2001, 12, 30),
                                        description='this is a test task',
                                        due_date=date(2002, 1, 1),
                                        frequency=Task.ONE_OFF,
                                        project=self.project,
                                        status=Task.OPEN_STATUS,
                                        title='test task',
                                        user='')
