from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from students.models import Student

class AuthenticationTests(TestCase):
    def setUp(self):
        # Create a test admin user
        self.admin_user = User.objects.create_superuser(
            username='admin', 
            email='admin@example.com', 
            password='adminpassword'
        )
        
        # Create a test student user
        self.student_user = User.objects.create_user(
            username='student1',
            email='student1@example.com',
            password='studentpassword',
            is_staff=False
        )
        Student.objects.create(
            user=self.student_user,
            name='Test Student',
            email='student1@example.com',
            phone='1234567890',
            course='BSc CSIT'
        )

    def test_login_page_renders(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login to CampusHub')

    def test_signup_page_renders(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Registration')

    def test_dashboard_redirects_unauthenticated(self):
        response = self.client.get(reverse('dashboard'))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_student_login_success(self):
        login_success = self.client.login(username='student1', password='studentpassword')
        self.assertTrue(login_success)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Dashboard')

    def test_admin_login_success(self):
        login_success = self.client.login(username='admin', password='adminpassword')
        self.assertTrue(login_success)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Dashboard')
