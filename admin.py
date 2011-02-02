from django.contrib import admin
from models import Project, Task, Work, Organisation, UserProfile

class ProjectAdmin(admin.ModelAdmin):
    pass

class TaskAdmin(admin.ModelAdmin):
    pass

class WorkAdmin(admin.ModelAdmin):
    pass

class OrganisationAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
