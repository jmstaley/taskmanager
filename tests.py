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

    def testGetTasks(self):
        project = Project.objects.get(pk='1')
        tasks = project.get_tasks()
        self.assertEqual(len(tasks), 2)

class TaskTestCase(TestCase):
    fixtures = ['taskmanager.json', 'users.json']

    def testGetTasksForUser(self):
        user = User.objects.get(pk='1')
        tasks = Task.objects.get_tasks_for_user(user)
        self.assertEqual(len(tasks), 2)
        for task in tasks:
            self.assertEqual(task.user, user)

    def testGetTasksOfFreq(self):
        tasks = Task.objects.get_tasks_of_freq(Task.ONE_OFF)
        self.assertEqual(len(tasks), 2)

class WorkTestCase(TestCase):
    fixtures = ['taskmanager.json', 'users.json']

    def testGetWorkForTask(self):
        task = Task.objects.get(pk='1')
        work = Work.objects.get_work_for_task(task)
        self.assertEqual(len(work), 1)
