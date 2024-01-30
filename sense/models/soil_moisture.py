from django.db import models

from sense.models import Sensor
from sense.models.services import SenseSoilMoisture


class SoilMoistureSensor(Sensor):
    # TODO: validate the inputs, for example with choices

    analog_pin = models.IntegerField(
        verbose_name="شماره پین آنالوگ",
    )

    digital_pin = models.IntegerField(
        verbose_name="شماره پین دیجیتال",
    )

    sense_class = SenseSoilMoisture

    class Meta:
        verbose_name = "سنسور رطوبت خاک"
        verbose_name_plural = "سنسورهای رطوبت خاک"
