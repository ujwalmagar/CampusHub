from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from students.models import Student
from events.models import Event
from registrations.models import Registration

class SecurityE2ETests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create Student A
        self.user_a = User.objects.create_user(username='studentA', password='password123')
        self.student_a = Student.objects.create(
            user=self.user_a, 
            name='Student A', 
            email='a@example.com', 
            phone='1111111111', 
            major='CS'
        )
        
        # Create Student B
        self.user_b = User.objects.create_user(username='studentB', password='password123')
        self.student_b = Student.objects.create(
            user=self.user_b, 
            name='Student B', 
            email='b@example.com', 
            phone='2222222222', 
            major='IT'
        )
        
        # Create Admin
        self.admin_user = User.objects.create_superuser(username='admin', password='password123', email='admin@example.com')
        
        # Create Event
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Desc',
            event_date='2027-01-01T10:00:00Z',
            location='Room 101',
            capacity=10,
            status='OPEN'
        )

    def test_csrf_protection(self):
        """Part 1: CSRF Test"""
        self.client.login(username='studentA', password='password123')
        # Attempt to POST without CSRF token
        response = self.client.post(reverse('student_task_update', args=[1]), {'task_status': 'COMPLETED'})
        # Django test client disables CSRF checks by default unless enforce_csrf_checks is True.
        # So we use a client with enforce_csrf_checks=True
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.login(username='studentA', password='password123')
        response = csrf_client.post(reverse('student_task_update', args=[1]), {'task_status': 'COMPLETED'})
        self.assertEqual(response.status_code, 403, "CSRF check failed: Request without CSRF token should be forbidden.")

    def test_xss_protection(self):
        """Part 2: XSS Test"""
        xss_payload = '<script>alert("XSS_TEST")</script>'
        self.event.title = xss_payload
        self.event.save()
        
        self.client.login(username='studentA', password='password123')
        response = self.client.get(reverse('event_list'))
        # Ensure the payload is escaped in the HTML
        self.assertNotContains(response, xss_payload)
        self.assertContains(response, '&lt;script&gt;alert(&quot;XSS_TEST&quot;)&lt;/script&gt;')

    def test_idor_view_registration(self):
        """Part 3: IDOR - View Registration"""
        reg_a = Registration.objects.create(student=self.student_a, event=self.event, status='PENDING')
        
        # Student A views own registration
        self.client.login(username='studentA', password='password123')
        response = self.client.get(reverse('registration-detail', args=[reg_a.pk]))
        self.assertEqual(response.status_code, 200)
        
        # Student B attempts to view Student A's registration
        self.client.logout()
        self.client.login(username='studentB', password='password123')
        response = self.client.get(reverse('registration-detail', args=[reg_a.pk]))
        self.assertEqual(response.status_code, 404, "IDOR Vulnerability: Student B could view Student A's registration.")

    def test_idor_cancel_registration(self):
        """Part 3: IDOR - Cancel Registration"""
        reg_a = Registration.objects.create(student=self.student_a, event=self.event, status='PENDING')
        
        # Student B attempts to cancel Student A's registration
        self.client.login(username='studentB', password='password123')
        response = self.client.delete(reverse('registration-detail', args=[reg_a.pk]))
        self.assertEqual(response.status_code, 404, "IDOR Vulnerability: Student B could cancel Student A's registration.")
        
        # Verify it wasn't cancelled
        reg_a.refresh_from_db()
        self.assertEqual(reg_a.status, 'PENDING')
        
        # Student A cancels own registration
        self.client.logout()
        self.client.login(username='studentA', password='password123')
        response = self.client.delete(reverse('registration-detail', args=[reg_a.pk]))
        self.assertEqual(response.status_code, 204)

    def test_registration_tampering(self):
        """Part 3: Registration Tampering"""
        self.client.login(username='studentA', password='password123')
        # Student A tries to register Student B by passing student_id=student_b.id
        response = self.client.post(reverse('registration-list'), {
            'event_id': self.event.event_id,
            'student_id': self.student_b.student_id
        })
        self.assertEqual(response.status_code, 201)
        
        # Verify the registration actually belongs to Student A, not Student B
        reg = Registration.objects.get(event=self.event)
        self.assertEqual(reg.student, self.student_a, "Tampering Vulnerability: Student A successfully registered Student B.")

    def test_role_authorization(self):
        """Part 6: Role Authorization"""
        self.client.login(username='studentA', password='password123')
        
        # Student attempts to access Admin dashboard
        response = self.client.get(reverse('admin_reports'))
        # Should redirect to login or show 403. Let's assume redirect to login or 403.
        self.assertIn(response.status_code, [302, 403], "Role Auth Failure: Student accessed admin route.")
        
        # Student attempts to access Event Manage
        response = self.client.get(reverse('event_manage'))
        self.assertIn(response.status_code, [302, 403], "Role Auth Failure: Student accessed event manage route.")
        
        # Admin accesses Admin route
        self.client.logout()
        self.client.login(username='admin', password='password123')
        response = self.client.get(reverse('event_manage'))
        self.assertEqual(response.status_code, 200)

