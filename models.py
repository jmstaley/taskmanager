from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    """Project for grouping tasks together"""
    description = models.TextField(blank=True)
    due_date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    def get_tasks(self):
        tasks = Task.objects.filter(project=self)
        return tasks

class TaskManager(models.Manager):
    def get_tasks_for_user(self, user):
        return self.filter(user=user)

    def get_tasks_of_freq(self, freq):
        return self.filter(frequency=freq)

class Task(models.Model):
    """Represents a piece of work to be done"""
    DAILY = 1
    TWO_DAILY = 2
    WEEKLY = 3
    FORTNIGHTLY = 4
    MONTHLY = 5
    ONE_OFF = 0
    FREQUENCY_CHOICES = (
        (DAILY, 'Daily'),
        (TWO_DAILY, 'Two Daily'),
        (WEEKLY, 'Weekly'),
        (FORTNIGHTLY, 'Fortnightly'),
        (MONTHLY, 'Monthly'),
        (ONE_OFF, 'One Off')
    )

    OPEN_STATUS = 1
    COMPLETED_STATUS = 2
    CLOSED_STATUS = 3
    LATE_STATUS = 4
    STATUS_CHOICES = (
        (OPEN_STATUS, 'Open'),
        (COMPLETED_STATUS, 'Completed'),
        (CLOSED_STATUS, 'Closed'),
        (LATE_STATUS, 'Late')
    )

    creation_date = models.DateField(auto_now_add=True, auto_now=True)
    description = models.TextField(blank=True)
    due_date = models.DateField(blank=True, null=True)
    frequency = models.IntegerField(choices=FREQUENCY_CHOICES, default=ONE_OFF)
    project = models.ForeignKey(Project)
    status = models.IntegerField(choices=STATUS_CHOICES, default=OPEN_STATUS)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    
    objects = TaskManager()

    class Meta:
        permissions = (
            ('can_change_status', 'Can change the status of the task'),
            ('can_close', 'Can close a task')
        )

    def __unicode__(self):
        return self.title

class WorkManager(models.Manager):
    def get_work_for_task(self, task):
        return self.filter(task=task)

class Work(models.Model):
    """Work done associated to a task"""
    user = models.ForeignKey(User)
    creation_date = models.DateField(auto_now_add=True, auto_now=True)
    task = models.ForeignKey(Task)
    comment = models.TextField(blank=True)

    objects = WorkManager()

    def __unicode__(self):
        return self.creation_date.strftime('%d/%m/%y')

class Organisation(models.Model):
    """Simple organisation object"""
    name = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    """Holds data on a user"""
    user = models.ForeignKey(User, unique=True)
    phone_number = models.CharField(max_length=255, blank=False)
    org = models.ForeignKey(Organisation)
