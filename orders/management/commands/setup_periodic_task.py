from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule

class Command(BaseCommand):
    help = 'Sets up periodic task for monitoring warehouse emails'

    def handle(self, *args, **options):
        # Ensure only one schedule exists for 1 minute
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=5,
            period=IntervalSchedule.MINUTES
        )
        # Ensure only one task exists
        PeriodicTask.objects.update_or_create(
            name='Monitor warehouse emails',
            defaults={
                'interval': schedule,
                'task': 'orders.tasks.monitor_warehouse_emails',
                'enabled': True
            }
        )
        self.stdout.write(self.style.SUCCESS('Periodic task set up successfully'))