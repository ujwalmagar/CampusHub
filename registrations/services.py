from django.core.exceptions import ValidationError
from .models import Registration
from events.models import Event

def register_for_event(student, event):
    """
    Registers a student for an event.
    Business Logic:
    1. Event must be OPEN.
    2. Registration is created in a PENDING state.
    3. The database UniqueConstraint prevents double registration.
    """
    if event.status != 'OPEN':
        raise ValidationError(f"Cannot register for an event with status: {event.status}")
    
    # We rely on the database-level UniqueConstraint to throw an IntegrityError 
    # if the student is already registered, ensuring strict data integrity.
    registration = Registration(
        student=student,
        event=event,
        status='PENDING'
    )
    
    # Validate the model before saving
    registration.full_clean()
    registration.save()
    
    return registration

from django.db import transaction, connections
import logging

logger = logging.getLogger(__name__)

def process_registrations():
    """
    Background task logic to process PENDING registrations.
    Uses select_for_update to lock rows and prevent race conditions.
    Safely handles connections when run in a raw Python thread.
    """
    processed_count = 0
    try:
        with transaction.atomic():
            # Find events with pending registrations first
            pending_event_ids = list(
                Registration.objects.filter(status='PENDING')
                .values_list('event_id', flat=True)
                .distinct()
            )
            
            # Lock only those specific events safely without using distinct() in the FOR UPDATE query
            events = Event.objects.filter(
                pk__in=pending_event_ids
            ).select_for_update()
            
            for event in events:
                # Count currently confirmed registrations safely inside the transaction
                confirmed_count = Registration.objects.filter(event=event, status='CONFIRMED').count()
                remaining_capacity = event.capacity - confirmed_count
                
                # Fetch pending registrations ordered by oldest first (FIFO)
                pending_regs = Registration.objects.filter(
                    event=event, 
                    status='PENDING'
                ).order_by('registered_at')
                
                for reg in pending_regs:
                    if remaining_capacity > 0:
                        reg.status = 'CONFIRMED'
                        reg.save()
                        remaining_capacity -= 1
                        processed_count += 1
                    else:
                        # Capacity is full. Leave them PENDING (acting as a waitlist).
                        break
                        
    except Exception as e:
        logger.error(f"Error processing registrations: {e}")
    finally:
        # Crucial for preventing connection leaks when running inside threading.Thread
        connections.close_all()
        
    return {"processed": processed_count}
