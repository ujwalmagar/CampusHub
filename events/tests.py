from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Event

class EventModelTests(TestCase):
    def test_create_valid_event(self):
        event = Event.objects.create(
            title="Valid Event",
            description="This should work",
            event_date=timezone.now(),
            location="Room 101",
            capacity=50,
            status="OPEN"
        )
        self.assertEqual(event.title, "Valid Event")

    def test_capacity_must_be_positive_model_validation(self):
        event = Event(
            title="Zero Capacity Event",
            description="Testing application layer validation",
            event_date=timezone.now(),
            location="Room 102",
            capacity=0,
            status="OPEN"
        )
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_capacity_must_be_positive_db_constraint(self):
        with self.assertRaises(IntegrityError):
            # We bypass full_clean() to test the CheckConstraint directly on save()
            Event.objects.create(
                title="Negative Capacity Event",
                description="Testing DB constraint",
                event_date=timezone.now(),
                location="Room 103",
                capacity=-5,
                status="OPEN"
            )
