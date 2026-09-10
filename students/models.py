from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    # We use a OneToOneField because one Auth User has exactly one Student profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    
    # We explicitly define student_id as the primary key to match the database spec
    student_id = models.AutoField(primary_key=True)
    
    name = models.CharField(max_length=255)
    # The email is technically on the User model too, but spec requires it here as well
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    course = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f"{self.name} ({self.course})"
