from django.contrib import admin
from . import models

# Custom admin class
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')

class CourseAdmin(admin.ModelAdmin):
        list_display = ('name', 'description')

# Register your models here.
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Lecturer, LecturerAdmin)
admin.site.register(models.Course, CourseAdmin)