from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'title', 'event_date', 'location', 'capacity', 'status')
    list_filter = ('status', 'event_date')
    search_fields = ('title', 'location')
