from time import sleep
import traceback
from typing import Optional

from django.core.management.base import BaseCommand
from django.db.models import Q, F, Case, When, DateTimeField
from django.utils import timezone

from monitor.models import SensorMonitor


class Command(BaseCommand):
    def run_one_task(self):
        qs = (
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
        monitor: Optional[SensorMonitor] = qs.first()
        if monitor is None:
            return
        monitor.monitor()

    def handle(self, *args, **options):
        print("scheduler has started")
        while True:
            try:
                print('waiting for 10 seconds...')
                sleep(10)
                self.run_one_task()
            except KeyboardInterrupt:
                print("Ended Monitoring with CTRL+C")
                break
            except Exception:
                print(traceback.format_exc())
