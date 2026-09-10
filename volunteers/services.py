from django.core.exceptions import ValidationError
from .models import VolunteerTask

def assign_volunteer_task(student, event, task_name):
    """
    Assigns a volunteer task to a student for a specific event.
    Business Logic:
    1. Event must be OPEN.
    2. Task is created in an ASSIGNED state.
    """
    if event.status != 'OPEN':
        raise ValidationError(f"Cannot assign volunteer tasks for an event with status: {event.status}")
    
    task = VolunteerTask(
        student=student,
        event=event,
        task_name=task_name,
        task_status='ASSIGNED'
    )
    
    task.full_clean()
    task.save()
    
    return task
