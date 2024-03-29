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
        related_name="monitor",
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
            sensor = self.sensor.concrete_instance
            data: "Sense.SenseData" = sensor.sense()
            if data is not None:
                SensorResult.objects.create(sensor=self.sensor, result=data.to_dict())
                sensor.update_figure()
            self.last_monitor = timezone.now()
            self.save(update_fields=["last_monitor"])

    class Meta:
        verbose_name = "پایشگر سنسور"
        verbose_name_plural = "پایشگران سنسورها"
