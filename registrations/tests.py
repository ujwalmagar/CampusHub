from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.management import call_command
from students.models import Student
from events.models import Event
from .models import Registration
from .services import register_for_event

class RegistrationServiceTests(TestCase):
    def setUp(self):
        # Create users and students
        self.user1 = User.objects.create_user(username='student1', password='password')
        self.student1 = Student.objects.create(user=self.user1, name="Student 1", email="s1@example.com", phone="123", course="CS")
        
        self.user2 = User.objects.create_user(username='student2', password='password')
        self.student2 = Student.objects.create(user=self.user2, name="Student 2", email="s2@example.com", phone="123", course="CS")
        
        # Create an event with a strict capacity of 1
        self.event = Event.objects.create(
            title="Limited Tech Talk", 
            event_date=timezone.now(), 
            location="Hall A", 
            capacity=1, 
            status="OPEN"
        )

    def test_register_for_event_creates_pending_status(self):
        # Test the service layer directly
        registration = register_for_event(self.student1, self.event)
        self.assertEqual(registration.status, 'PENDING')
        self.assertEqual(Registration.objects.count(), 1)

    def test_process_registrations_command_respects_capacity(self):
        # Simulate two students trying to register for an event with capacity = 1
        # First they both register successfully as PENDING
        reg1 = register_for_event(self.student1, self.event)
        
        # By bypassing the service layer for the second one (which would normally fail on unique constraint if same student, 
        # but here we use a different student)
        reg2 = register_for_event(self.student2, self.event)
        
        self.assertEqual(Registration.objects.filter(status='PENDING').count(), 2)
        
        # Run the background processor command
        call_command('process_registrations')
        
        # Refresh from DB
        reg1.refresh_from_db()
        reg2.refresh_from_db()
        
        # Since it processes in FIFO order, reg1 should be CONFIRMED and reg2 should be CANCELLED
        self.assertEqual(reg1.status, 'CONFIRMED')
        self.assertEqual(reg2.status, 'CANCELLED')
