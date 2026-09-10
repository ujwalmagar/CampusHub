from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'course', 'email', 'phone')
    search_fields = ('name', 'email', 'course')
