from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Student
from events.models import Event
from registrations.models import Registration
from volunteers.models import VolunteerTask
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seeds the database with realistic demo data for Phase 7'

    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding...")

        # Clear existing non-staff users and data to prevent unique constraint errors during multiple runs
        User.objects.filter(is_staff=False).delete()
        Event.objects.all().delete()
        
        # 1 & 2. Create 10 Students (and their User accounts)
        student_data = [
            ('Ram Sharma', 'ram@example.com', '9800000001', 'BSc CSIT'),
            ('Sita Thapa', 'sita@example.com', '9800000002', 'BCA'),
            ('Hari Poudel', 'hari@example.com', '9800000003', 'BIM'),
            ('Gita Rai', 'gita@example.com', '9800000004', 'BSc CSIT'),
            ('Shyam Karki', 'shyam@example.com', '9800000005', 'BIT'),
            ('Mina Shrestha', 'mina@example.com', '9800000006', 'BCA'),
            ('Sunil Gurung', 'sunil@example.com', '9800000007', 'BIM'),
            ('Nita Magar', 'nita@example.com', '9800000008', 'BSc CSIT'),
            ('Bishal Bista', 'bishal@example.com', '9800000009', 'BIT'),
            ('Puja Tamang', 'puja@example.com', '9800000010', 'BCA'),
        ]
        
        students = []
        for name, email, phone, course in student_data:
            user = User.objects.create_user(username=email, email=email, password='password123')
            student = Student.objects.create(user=user, name=name, email=email, phone=phone, course=course)
            students.append(student)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully created 10 students.'))

        # 3. Create 5 Events
        now = timezone.now()
        events_data = [
            ('Blood Donation Camp', 'Annual campus blood donation program.', now + timedelta(days=10), 'College Hall', 50, 'OPEN'),
            ('Web Development Workshop', '3-day React and Django crash course.', now + timedelta(days=15), 'Computer Lab 1', 30, 'OPEN'),
            ('College Sports Day', 'Inter-department sports competition.', now + timedelta(days=20), 'College Ground', 200, 'OPEN'),
            ('Career Guidance Seminar', 'Seminar featuring IT industry professionals.', now + timedelta(days=5), 'Auditorium', 100, 'CLOSED'),
            ('Cultural Festival', 'End of semester cultural performances.', now - timedelta(days=5), 'Main Stage', 150, 'COMPLETED'),
        ]
        
        events = []
        for title, desc, date, loc, cap, status in events_data:
            event = Event.objects.create(title=title, description=desc, event_date=date, location=loc, capacity=cap, status=status)
            events.append(event)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully created 5 events.'))

        # 4. Create 15 Registrations
        reg_data = [
            (0, 0, 'CONFIRMED'), (1, 0, 'CONFIRMED'), (2, 0, 'PENDING'), (3, 0, 'CANCELLED'), # Event 0
            (0, 1, 'CONFIRMED'), (4, 1, 'PENDING'), (5, 1, 'CONFIRMED'),                     # Event 1
            (6, 2, 'CONFIRMED'), (7, 2, 'CONFIRMED'), (8, 2, 'PENDING'), (9, 2, 'CONFIRMED'),# Event 2
            (0, 3, 'CONFIRMED'), (1, 3, 'CONFIRMED'),                                        # Event 3
            (4, 4, 'CONFIRMED'), (9, 4, 'CONFIRMED'),                                        # Event 4
        ]
        
        for s_idx, e_idx, status in reg_data:
            Registration.objects.create(student=students[s_idx], event=events[e_idx], status=status)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully created 15 registrations.'))

        # 5. Create 8 Volunteer Tasks
        task_data = [
            (0, 0, 'Registration Desk', 'ASSIGNED'),
            (1, 0, 'Medical Assistance Team', 'IN_PROGRESS'),
            (2, 1, 'Technical Support', 'ASSIGNED'),
            (3, 1, 'Guest Coordination', 'ASSIGNED'),
            (4, 2, 'Crowd Management', 'ASSIGNED'),
            (5, 2, 'Referee Assistant', 'ASSIGNED'),
            (6, 3, 'Stage Management', 'COMPLETED'),
            (7, 4, 'Photography', 'COMPLETED'),
        ]
        
        for s_idx, e_idx, t_name, t_status in task_data:
            VolunteerTask.objects.create(student=students[s_idx], event=events[e_idx], task_name=t_name, task_status=t_status)

        self.stdout.write(self.style.SUCCESS(f'Successfully created 8 volunteer tasks.'))
        self.stdout.write(self.style.SUCCESS(f'Database seed complete! You can log in with any student email (e.g. ram@example.com) and password "password123".'))
