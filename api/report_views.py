from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q

from events.models import Event
from students.models import Student
from registrations.models import Registration
from volunteers.models import VolunteerTask

@api_view(['GET'])
@permission_classes([IsAdminUser])
def event_participation_report(request, pk):
    """
    Complex Query 1: Event Participation Report
    Returns aggregate stats for a specific event.
    Requires Admin privileges.
    """
    event = get_object_or_404(Event, pk=pk)
    
    # We can use Django's aggregation, or just count using the ORM.
    total_registrations = Registration.objects.filter(event=event).count()
    confirmed_registrations = Registration.objects.filter(event=event, status='CONFIRMED').count()
    cancelled_registrations = Registration.objects.filter(event=event, status='CANCELLED').count()
    
    volunteer_count = VolunteerTask.objects.filter(event=event).count()
    completed_tasks = VolunteerTask.objects.filter(event=event, task_status='COMPLETED').count()
    
    return Response({
        "event": {
            "id": event.event_id,
            "title": event.title
        },
        "total_registrations": total_registrations,
        "confirmed_registrations": confirmed_registrations,
        "cancelled_registrations": cancelled_registrations,
        "volunteer_count": volunteer_count,
        "completed_tasks": completed_tasks
    })

@api_view(['GET'])
@permission_classes([IsAdminUser])
def student_participation_report(request, pk):
    """
    Complex Query 2: Student Participation Report
    Returns aggregate stats for a specific student across all events.
    Requires Admin privileges.
    """
    student = get_object_or_404(Student, pk=pk)
    
    total_events = Registration.objects.filter(student=student).count()
    confirmed_events = Registration.objects.filter(student=student, status='CONFIRMED').count()
    
    volunteer_tasks = VolunteerTask.objects.filter(student=student).count()
    completed_tasks = VolunteerTask.objects.filter(student=student, task_status='COMPLETED').count()
    
    return Response({
        "student": {
            "id": student.student_id,
            "name": student.name,
            "course": student.course
        },
        "total_events": total_events,
        "confirmed_events": confirmed_events,
        "volunteer_tasks": volunteer_tasks,
        "completed_tasks": completed_tasks
    })
