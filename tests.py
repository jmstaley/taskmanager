from django.test import TestCase
from django.contrib.auth.models import User

from taskmanager.models import Project, Task, Work, Organisation, UserProfile

from datetime import date

class ProjectTest(TestCase):
    fixtures = ['taskmanager.json', ]

    def testName(self):
        project = Project.objects.get(pk='1')
        self.assertEqual(project.name, 'Test Project')

    def testDueDate(self):
        project = Project.objects.get(pk='1')
        self.assertEqual(project.due_date, date(2099, 01, 01))
