from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from events.models import Event
from students.models import Student
from registrations.models import Registration
from volunteers.models import VolunteerTask

@staff_member_required
def admin_reports(request):
    event_reports = []
    for event in Event.objects.all()[:10]:
        total_regs = Registration.objects.filter(event=event).count()
        confirmed = Registration.objects.filter(event=event, status='CONFIRMED').count()
        cancelled = Registration.objects.filter(event=event, status='CANCELLED').count()
        volunteers = VolunteerTask.objects.filter(event=event).count()
        completed = VolunteerTask.objects.filter(event=event, task_status='COMPLETED').count()
        
        event_reports.append({
            'event': event,
            'total_registrations': total_regs,
            'confirmed_registrations': confirmed,
            'cancelled_registrations': cancelled,
            'total_volunteers': volunteers,
            'completed_volunteer_tasks': completed
        })
        
    student_reports = []
    for student in Student.objects.all()[:10]:
        total_events = Registration.objects.filter(student=student).count()
        confirmed_events = Registration.objects.filter(student=student, status='CONFIRMED').count()
        volunteer_tasks = VolunteerTask.objects.filter(student=student).count()
        completed_tasks = VolunteerTask.objects.filter(student=student, task_status='COMPLETED').count()
        
        student_reports.append({
            'student': student,
            'total_events_registered': total_events,
            'confirmed_events': confirmed_events,
            'total_volunteer_tasks': volunteer_tasks,
            'completed_volunteer_tasks': completed_tasks
        })
        
    context = {
        'event_reports': event_reports,
        'student_reports': student_reports
    }
    return render(request, 'admin/reports.html', context)
