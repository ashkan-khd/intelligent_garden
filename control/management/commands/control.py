from time import sleep
import traceback
from typing import Optional

from django.core.management.base import BaseCommand
from django.db.models import F
from control.models import SensorBuzz


class Command(BaseCommand):
    def run_one_task(self):
        qs = SensorBuzz.objects.filter(on=True).order_by(
            F("last_effort").asc(nulls_first=True)
        )
        buzz: Optional[SensorBuzz] = qs.first()
        if buzz is None:
            return
        buzz.try_buzz()

    def handle(self, *args, **options):
        print("control scheduler has started")
        while True:
            try:
                print('waiting for 10 seconds...')
                sleep(15)
                self.run_one_task()
            except KeyboardInterrupt:
                print("Ended Monitoring with CTRL+C")
                break
            except Exception:
                print(traceback.format_exc())
