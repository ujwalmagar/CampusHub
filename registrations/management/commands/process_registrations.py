from django.core.management.base import BaseCommand
from django.db import transaction
from registrations.models import Registration
from events.models import Event

class Command(BaseCommand):
    help = 'Processes PENDING registrations and confirms them based on event capacity'

    def handle(self, *args, **options):
        # Fetch all pending registrations, ordered by when they were registered (FIFO)
        pending_registrations = Registration.objects.filter(status='PENDING').order_by('registered_at')
        
        if not pending_registrations.exists():
            self.stdout.write(self.style.SUCCESS('No pending registrations to process.'))
            return

        processed_count = 0
        cancelled_count = 0

        for registration in pending_registrations:
            try:
                # Wrap the processing of each individual registration in an atomic transaction
                with transaction.atomic():
                    # select_for_update() locks the Event row so no other background task
                    # or process can read/write to it until this transaction completes.
                    # This completely prevents race conditions.
                    event = Event.objects.select_for_update().get(pk=registration.event_id)

                    # Calculate current confirmed registrations for this specific event
                    current_confirmed = Registration.objects.filter(
                        event=event, 
                        status='CONFIRMED'
                    ).count()

                    if current_confirmed < event.capacity:
                        registration.status = 'CONFIRMED'
                        registration.save()
                        self.stdout.write(self.style.SUCCESS(f'Confirmed registration {registration.registration_id} for event {event.title}'))
                        processed_count += 1
                    else:
                        registration.status = 'CANCELLED'
                        registration.save()
                        self.stdout.write(self.style.WARNING(f'Cancelled registration {registration.registration_id} for event {event.title} (Capacity Full)'))
                        cancelled_count += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing registration {registration.registration_id}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'Process complete. Confirmed: {processed_count}, Cancelled: {cancelled_count}'))
