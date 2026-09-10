from django.contrib import admin
from .models import VolunteerTask

@admin.register(VolunteerTask)
class VolunteerTaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'task_name', 'event', 'student', 'task_status')
    list_filter = ('task_status',)
    search_fields = ('task_name', 'student__name', 'event__title')
