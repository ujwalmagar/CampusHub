from rest_framework import serializers
from django.contrib.auth.models import User
from students.models import Student
from events.models import Event
from registrations.models import Registration
from volunteers.models import VolunteerTask

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'user', 'name', 'email', 'phone', 'course', 'created_at']
        read_only_fields = ['student_id', 'user', 'created_at']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['event_id', 'title', 'description', 'event_date', 'location', 'capacity', 'status', 'created_at']
        read_only_fields = ['event_id', 'created_at']
    
    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Capacity must be greater than 0.")
        return value

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['registration_id', 'student', 'event', 'registered_at', 'status']
        read_only_fields = ['registration_id', 'registered_at', 'status']

class VolunteerTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerTask
        fields = ['task_id', 'event', 'student', 'task_name', 'task_status', 'created_at']
        read_only_fields = ['task_id', 'created_at']
