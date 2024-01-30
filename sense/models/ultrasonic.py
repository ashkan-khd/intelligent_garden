from django.db import models

from sense.models import Sensor
from sense.models.services import SenseWaterHeightPercentage


class UltrasonicSensor(Sensor):
    trig_pin = models.IntegerField(verbose_name="پین trig")
    echo_pin = models.IntegerField(verbose_name="پین echo")

    total_height_cm = models.IntegerField(verbose_name='ارتفاع مخزن', help_text='به سانتی‌متر وارد کنید.')

    sense_class = SenseWaterHeightPercentage

    class Meta:
        verbose_name = "سنسور اولتراسونیک"
        verbose_name_plural = "سنسور‌های اولتراسونیک"
