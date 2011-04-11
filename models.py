from django.db import models
from django.contrib.auth.models import User

class ProjectManager(models.Manager):
    def get_organisation_projects(self, org):
        return self.filter(organisation=org)

class Project(models.Model):
    """Project for grouping tasks together"""
    description = models.TextField(blank=True)
    due_date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=255)
    organisation = models.ForeignKey('Organisation')

    objects = ProjectManager()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('project_detail', (), {'project_id': self.id,})

class TaskManager(models.Manager):
    def get_tasks_for_user(self, user):
        return self.filter(user=user)

    def unassigned_tasks(self, org):
        return self.filter(user=None, project__organisation=org)

    def get_tasks_of_freq(self, freq):
        return self.filter(frequency=freq)

    def get_tasks_for_project(self, project_id):
        return self.filter(project__id=project_id)

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
    project = models.ForeignKey(Project, blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=OPEN_STATUS)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, blank=True, null=True)
    creator = models.ForeignKey(User, related_name="creator")
    
    objects = TaskManager()

    class Meta:
        permissions = (
            ('can_change_status', 'Can change the status of the task'),
            ('can_close', 'Can close a task'),
            ('can_assign', 'Can assign a task to a user'),
        )

    def __unicode__(self):
        return self.title

    def get_status_str(self):
        return self.STATUS_CHOICES[self.status-1][1]

    @models.permalink
    def get_absolute_url(self):
        return ('task_detail', (), {'task_id': self.id,})

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

    def __unicode__(self):
        return self.user.username
