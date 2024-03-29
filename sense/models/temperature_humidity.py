from django.db import models

from sense.models import Sensor
from sense.models.services import SenseTemperatureHumidity, DrawTemperatureHumidityFig
from utility.models import Choices


class TemperatureHumiditySensor(Sensor):
    class Types(Choices):
        DHT22 = Choices.Choice("DHT22", "DHT22")

    tp = models.CharField(choices=Types.get_choices(), verbose_name="نوع سنسور", max_length=128)

    am2302_pin = models.IntegerField(verbose_name="پین am2302")

    sense_class = SenseTemperatureHumidity
    fig_class = DrawTemperatureHumidityFig

    class Meta:
        verbose_name = "سنسور دما و رطوبت"
        verbose_name_plural = "سنسورهای دما و رطوبت"
