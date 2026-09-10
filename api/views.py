from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from students.models import Student
from events.models import Event
from registrations.models import Registration
from volunteers.models import VolunteerTask

from .serializers import (
    StudentSerializer, 
    EventSerializer, 
    RegistrationSerializer, 
    VolunteerTaskSerializer
)

from registrations.services import register_for_event, process_registrations
import threading
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        """Show all events registered by a particular student."""
        student = self.get_object()
        registrations = Registration.objects.filter(student=student).select_related('event')
        
        events_data = []
        for reg in registrations:
            events_data.append({
                "id": reg.event.event_id,
                "title": reg.event.title,
                "event_date": reg.event.event_date,
                "location": reg.event.location,
                "registration_status": reg.status
            })
            
        return Response({
            "student": {
                "id": student.student_id,
                "name": student.name
            },
            "events": events_data
        })

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    # Only admins can create/update/delete events
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def registrations(self, request, pk=None):
        """Show all students registered for an event."""
        event = self.get_object()
        registrations = Registration.objects.filter(event=event).select_related('student')
        
        students_data = []
        for reg in registrations:
            students_data.append({
                "id": reg.student.student_id,
                "name": reg.student.name,
                "email": reg.student.email,
                "registration_status": reg.status
            })
            
        return Response({
            "event": {
                "id": event.event_id,
                "title": event.title
            },
            "students": students_data
        })

    @action(detail=True, methods=['get'], url_path='volunteer-tasks')
    def volunteer_tasks(self, request, pk=None):
        """Show volunteer assignments for an event."""
        event = self.get_object()
        tasks = VolunteerTask.objects.filter(event=event).select_related('student')
        
        tasks_data = []
        for task in tasks:
            tasks_data.append({
                "student_name": task.student.name,
                "task_name": task.task_name,
                "task_status": task.task_status
            })
            
        return Response({
            "event": {
                "id": event.event_id,
                "title": event.title
            },
            "volunteer_tasks": tasks_data
        })


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Enforce ownership: normal students can only view/modify their own registrations.
        Admins can view all registrations.
        """
        if self.request.user.is_staff:
            return Registration.objects.all()
        return Registration.objects.filter(student=self.request.user.student_profile)

    def create(self, request, *args, **kwargs):
        event_id = request.data.get('event_id')
        
        if request.user.is_staff:
            student_id = request.data.get('student_id')
            if not student_id:
                return Response({"error": "student_id is required for admins."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                student = Student.objects.get(pk=student_id)
            except Student.DoesNotExist:
                return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                student = request.user.student_profile
            except Exception:
                return Response({"error": "User does not have an associated student profile."}, status=status.HTTP_403_FORBIDDEN)

        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Enforce business rules strictly through the service layer
            registration = register_for_event(student, event)
            serializer = self.get_serializer(registration)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            # Duplicate registration triggers database constraint
            return Response({"error": "Student is already registered for this event."}, status=status.HTTP_409_CONFLICT)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def process(self, request):
        """
        Background task endpoint to process PENDING registrations.
        Uses threading to run asynchronously and return immediately.
        """
        thread = threading.Thread(target=process_registrations)
        thread.start()
        
        return Response(
            {"status": "Processing started in background"}, 
            status=status.HTTP_202_ACCEPTED
        )

class VolunteerTaskViewSet(viewsets.ModelViewSet):
    queryset = VolunteerTask.objects.all()
    serializer_class = VolunteerTaskSerializer
    permission_classes = [IsAuthenticated]
