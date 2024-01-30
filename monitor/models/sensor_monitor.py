from turtle import update
from typing import TYPE_CHECKING
from django.db import models, transaction
from django.utils import timezone

from monitor.models import SensorResult

if TYPE_CHECKING:
    from sense.models.services import Sense


class SensorMonitor(models.Model):
    sensor = models.OneToOneField(
        to="sense.Sensor",
        related_name="monitors",
        on_delete=models.PROTECT,
        verbose_name="سنسور مربوطه",
    )

    last_monitor = models.DateTimeField(
        verbose_name="آخرین پایش",
        null=True,
        blank=True,
    )

    time_between_sense = models.DurationField(
        verbose_name="مدت زمان تا پایش سنسور",
    )

    def monitor(self):
        with transaction.atomic():
            data: "Sense.SenseData" = self.sensor.sense()
            if data is not None:
                SensorResult.objects.create(sensor=self.sensor, result=data.to_json())
            self.last_monitor = timezone.now()
            self.save(update_fields=["last_monitor"])

    class Meta:
        verbose_name = "پایشگر سنسور"
        verbose_name_plural = "پایشگران سنسورها"
