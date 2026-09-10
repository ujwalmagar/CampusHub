from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.models import User

from students.models import Student
from events.models import Event
from registrations.models import Registration

class APISecurityAndBusinessRulesTests(APITestCase):
    def setUp(self):
        # APITestCase automatically provides a correctly-typed self.client
        
        # Create staff user for admin actions
        self.admin_user = User.objects.create_user(username='admin', password='password', is_staff=True)
        
        # Create student 1
        self.student_user = User.objects.create_user(username='student1', password='password')
        self.student1 = Student.objects.create(
            user=self.student_user, 
            name="Student 1", 
            email="s1@example.com", 
            phone="123", 
            course="CS"
        )
        
        # Create event
        self.event = Event.objects.create(
            title="API Test Event", 
            event_date=timezone.now(), 
            location="Hall", 
            capacity=1, 
            status="OPEN"
        )

    def test_public_access_is_rejected(self):
        """Proof that the API is not public, satisfying AGENTS.md Rule 5"""
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_can_view_events(self):
        """Proof that authenticated users can view events"""
        # pyrefly: ignore [missing-attribute]
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # pyrefly: ignore [missing-attribute]
        self.assertEqual(len(response.data), 1)

    def test_duplicate_registration_returns_409_conflict(self):
        """Proof that docs/api.md Section 20 error handling is implemented"""
        # pyrefly: ignore [missing-attribute]
        self.client.force_authenticate(user=self.student_user)
        
        # First registration (should succeed)
        response1 = self.client.post('/api/registrations/', {
            'student_id': self.student1.student_id,
            'event_id': self.event.event_id
        })
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Second registration for same event (should fail with 409)
        response2 = self.client.post('/api/registrations/', {
            'student_id': self.student1.student_id,
            'event_id': self.event.event_id
        })
        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
        # pyrefly: ignore [missing-attribute]
        self.assertIn('error', response2.data)
        
    def test_complex_query_event_participation(self):
        """Proof that Complex Query 1 works and requires admin"""
        # Create a registration first
        Registration.objects.create(student=self.student1, event=self.event, status='CONFIRMED')
        
        # Unauthenticated should fail (DRF Session Auth returns 403 for unauthenticated)
        response = self.client.get(f'/api/reports/events/{self.event.event_id}/participation/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Student should fail (requires IsAdminUser)
        # pyrefly: ignore [missing-attribute]
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(f'/api/reports/events/{self.event.event_id}/participation/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin should succeed
        # pyrefly: ignore [missing-attribute]
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'/api/reports/events/{self.event.event_id}/participation/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # pyrefly: ignore [missing-attribute]
        self.assertEqual(response.data['confirmed_registrations'], 1)
        # pyrefly: ignore [missing-attribute]
        self.assertEqual(response.data['event']['title'], 'API Test Event')

    def test_background_processing_respects_capacity(self):
        """Proof that Phase 8 background processing enforces capacity limits safely."""
        self.assertEqual(self.event.capacity, 1)
        
        # Create a second student
        student2_user = User.objects.create_user(username='student2', password='password')
        student2 = Student.objects.create(
            user=student2_user, name="Student 2", email="s2@example.com", phone="456", course="CS"
        )
        
        # Create two PENDING registrations manually for the same event
        Registration.objects.create(student=self.student1, event=self.event, status='PENDING')
        Registration.objects.create(student=student2, event=self.event, status='PENDING')
        
        # Trigger processing directly (avoiding threading issues in SQLite TestCase transactions)
        from registrations.services import process_registrations
        result = process_registrations()
        
        # Only 1 should be processed because capacity is 1
        self.assertEqual(result['processed'], 1)
        self.assertEqual(Registration.objects.filter(event=self.event, status='CONFIRMED').count(), 1)
        self.assertEqual(Registration.objects.filter(event=self.event, status='PENDING').count(), 1)
        
        # Verify the API endpoint triggers correctly for Admin
        # pyrefly: ignore [missing-attribute]
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post('/api/registrations/process/')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        # pyrefly: ignore [missing-attribute]
        self.assertEqual(response.data['status'], "Processing started in background")
