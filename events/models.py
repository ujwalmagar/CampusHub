from django.db import models
from django.core.exceptions import ValidationError

class Event(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'events'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(capacity__gt=0),
                name='capacity_positive'
            )
        ]

    def clean(self):
        super().clean()
        if self.capacity is not None and self.capacity <= 0:
            raise ValidationError({'capacity': 'Capacity must be greater than 0.'})

    def __str__(self):
        return self.title
