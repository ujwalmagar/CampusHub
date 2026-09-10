from django.contrib import admin
from .models import Registration

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('registration_id', 'student', 'event', 'status', 'registered_at')
    list_filter = ('status', 'registered_at')
    search_fields = ('student__name', 'event__title')
