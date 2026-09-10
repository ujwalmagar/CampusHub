from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from students.models import Student
from events.models import Event
from .models import VolunteerTask

class VolunteerModelTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='volunteer1', password='password')
        self.student = Student.objects.create(
            user=user, name="Jane Doe", email="jane@example.com", phone="123", course="IT"
        )
        self.event = Event.objects.create(
            title="Charity Run", event_date=timezone.now(), location="Track", capacity=50, status="OPEN"
        )

    def test_volunteer_task_creation(self):
        task = VolunteerTask.objects.create(
            event=self.event,
            student=self.student,
            task_name="Hand out water",
            task_status="ASSIGNED"
        )
        self.assertEqual(task.task_name, "Hand out water")
        self.assertEqual(task.event.title, "Charity Run")
        self.assertEqual(task.student.name, "Jane Doe")
