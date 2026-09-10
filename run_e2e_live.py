import os
import django
import sys

# Setup Django environment to use the ACTUAL database, not the test database
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from students.models import Student
from events.models import Event
from registrations.models import Registration

def run_tests():
    print("--- STARTING E2E SECURITY TESTS AGAINST LIVE DB ---")
    
    # 1. Setup Test Data
    print("Setting up test data...")
    user_a, _ = User.objects.get_or_create(username='e2e_studentA', email='a@e2e.com')
    user_a.set_password('password123')
    user_a.save()
    student_a, _ = Student.objects.get_or_create(user=user_a, name='Student A', email='a@e2e.com', phone='111', course='CS')

    user_b, _ = User.objects.get_or_create(username='e2e_studentB', email='b@e2e.com')
    user_b.set_password('password123')
    user_b.save()
    student_b, _ = Student.objects.get_or_create(user=user_b, name='Student B', email='b@e2e.com', phone='222', course='IT')

    admin, _ = User.objects.get_or_create(username='e2e_admin', email='admin@e2e.com')
    admin.set_password('password123')
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()

    event, _ = Event.objects.get_or_create(
        title='E2E Test Event',
        defaults={
            'description': 'Test Desc',
            'event_date': '2027-01-01T10:00:00Z',
            'location': 'Room 101',
            'capacity': 10,
            'status': 'OPEN'
        }
    )
    
    # Clear previous registrations for this event to be safe
    Registration.objects.filter(event=event).delete()
    
    results = {}

    # --- PART 1: CSRF TEST ---
    print("\n--- Running PART 1: CSRF TEST ---")
    # Using Client with enforce_csrf_checks=True
    csrf_client = Client(enforce_csrf_checks=True)
    csrf_client.login(username='e2e_studentA', password='password123')
    
    # Attempt POST without CSRF token
    response = csrf_client.post('/accounts/login/', {'username': 'test', 'password': '123'})
    if response.status_code == 403:
        print("CSRF Test: PASS (Request rejected with 403)")
        results['CSRF'] = 'PASS'
    else:
        print(f"CSRF Test: FAIL (Status {response.status_code})")
        results['CSRF'] = 'FAIL'


    # --- PART 2: XSS TEST ---
    print("\n--- Running PART 2: XSS TEST ---")
    xss_payload = '<script>alert("XSS_TEST")</script>'
    event.title = xss_payload
    event.save()
    
    client_a = Client()
    client_a.login(username='e2e_studentA', password='password123')
    response = client_a.get(reverse('event_list'))
    content = response.content.decode('utf-8')
    if xss_payload not in content and '&lt;script&gt;alert(&quot;XSS_TEST&quot;)&lt;/script&gt;' in content:
        print("XSS Test: PASS (Payload escaped)")
        results['XSS'] = 'PASS'
    else:
        print("XSS Test: FAIL (Payload not correctly escaped)")
        results['XSS'] = 'FAIL'
        
    event.title = 'E2E Test Event'
    event.save()


    # --- PART 3: IDOR TESTS ---
    print("\n--- Running PART 3: IDOR TESTS ---")
    reg_a = Registration.objects.create(student=student_a, event=event, status='PENDING')
    
    client_b = Client()
    client_b.login(username='e2e_studentB', password='password123')
    
    # Test 1 & 2: View Registration
    res_a = client_a.get(reverse('registration-detail', args=[reg_a.pk]))
    res_b = client_b.get(reverse('registration-detail', args=[reg_a.pk]))
    
    if res_a.status_code == 200 and res_b.status_code == 404:
        print("IDOR View Registration: PASS (Student B got 404)")
        results['IDOR - view own registration'] = 'PASS'
        results['IDOR - view another registration'] = 'PASS'
    else:
        print(f"IDOR View Registration: FAIL (Student A: {res_a.status_code}, Student B: {res_b.status_code})")
        results['IDOR - view own registration'] = 'FAIL'
        results['IDOR - view another registration'] = 'FAIL'

    # Test 3: Cancel another's registration
    res_cancel_b = client_b.delete(reverse('registration-detail', args=[reg_a.pk]))
    if res_cancel_b.status_code == 404:
        print("IDOR Cancel Another Registration: PASS (Student B got 404)")
        results['IDOR - cancel another registration'] = 'PASS'
    else:
        print(f"IDOR Cancel Another Registration: FAIL (Status {res_cancel_b.status_code})")
        results['IDOR - cancel another registration'] = 'FAIL'
        
    # Test 4: Cancel own registration
    res_cancel_a = client_a.delete(reverse('registration-detail', args=[reg_a.pk]))
    if res_cancel_a.status_code == 204:
        print("IDOR Cancel Own Registration: PASS (Student A got 204)")
        results['IDOR - cancel own registration'] = 'PASS'
    else:
        print(f"IDOR Cancel Own Registration: FAIL (Status {res_cancel_a.status_code})")
        results['IDOR - cancel own registration'] = 'FAIL'

    # Test 5: Registration Tampering
    # Student A tries to register Student B
    res_tamper = client_a.post(reverse('registration-list'), {
        'event_id': event.event_id,
        'student_id': student_b.student_id
    })
    if res_tamper.status_code == 201:
        # Check who actually got registered
        new_reg = Registration.objects.get(event=event)
        if new_reg.student == student_a:
            print("Registration Tampering: PASS (Registered Student A despite payload)")
            results['Registration tampering'] = 'PASS'
        else:
            print("Registration Tampering: FAIL (Student B was registered!)")
            results['Registration tampering'] = 'FAIL'
    else:
        print(f"Registration Tampering: FAIL (Status {res_tamper.status_code})")
        results['Registration tampering'] = 'FAIL'

    # --- PART 6: ROLE AUTHORIZATION ---
    print("\n--- Running PART 6: ROLE AUTHORIZATION ---")
    res_auth_a = client_a.get(reverse('event_manage'))
    admin_client = Client()
    admin_client.login(username='e2e_admin', password='password123')
    res_auth_admin = admin_client.get(reverse('event_manage'))
    
    if res_auth_a.status_code in [302, 403] and res_auth_admin.status_code == 200:
        print("Role Authorization: PASS")
        results['Role authorization'] = 'PASS'
    else:
        print(f"Role Authorization: FAIL (Student A: {res_auth_a.status_code}, Admin: {res_auth_admin.status_code})")
        results['Role authorization'] = 'FAIL'

    print("\n--- FINAL RESULTS ---")
    for test, res in results.items():
        print(f"{test}: {res}")

if __name__ == '__main__':
    run_tests()
