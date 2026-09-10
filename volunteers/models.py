from django.db import models
from students.models import Student
from events.models import Event

class VolunteerTask(models.Model):
    STATUS_CHOICES = [
        ('ASSIGNED', 'Assigned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    task_id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='volunteer_tasks')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='volunteer_tasks')
    task_name = models.CharField(max_length=255)
    task_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ASSIGNED')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'volunteer_tasks'

    def __str__(self):
        return f"Task: {self.task_name} (Event: {self.event.title})"
