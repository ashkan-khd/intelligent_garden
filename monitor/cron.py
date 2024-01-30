from django.db.models import Q, F, Case, When, DateTimeField
from django.utils import timezone
from django_cron import CronJobBase, Schedule

from monitor.models.sensor_monitor import SensorMonitor


class MonitorCronJob(CronJobBase):
    RUN_EVERY_MINS = 0.1  # every 6 seconds

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "monitor.sensors"  # a unique code

    def get_queryset(self):
        return (
            SensorMonitor.objects.annotate(
                next_monitor=Case(
                    When(
                        Q(last_monitor__isnull=True),
                        then=None,
                    ),
                    default=F("last_monitor") + F("time_between_sense"),
                    output_field=DateTimeField(null=True),
                )
            )
            .filter(Q(next_monitor__isnull=True) | Q(next_monitor__lte=timezone.now()))
            .order_by(F("next_monitor").asc(nulls_first=True))
        )

    def do(self):
        monitor: SensorMonitor = self.get_queryset().first()
        if monitor is None:
            return
        monitor.monitor()
