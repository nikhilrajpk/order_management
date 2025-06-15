from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule

class Command(BaseCommand):
    help = 'Sets up periodic task for monitoring warehouse emails'

    def handle(self, *args, **options):
        schedule, created = IntervalSchedule.objects.update_or_create(
            every=1,
            period=IntervalSchedule.MINUTES
        )
        PeriodicTask.objects.update_or_create(
            interval=schedule,
            name='Monitor warehouse emails',
            task='orders.tasks.monitor_warehouse_emails'
        )
        self.stdout.write(self.style.SUCCESS('Periodic task set up successfully'))