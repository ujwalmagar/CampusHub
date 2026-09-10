from django.db import models
from students.models import Student
from events.models import Event

class Registration(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    registration_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        db_table = 'registrations'
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'event'],
                name='unique_student_event_registration'
            )
        ]

    def __str__(self):
        return f"Registration: {self.student.name} for {self.event.title}"
