from typing import TYPE_CHECKING, List, Optional, Type

from django.core.files import File
from django.db import models

from sense.models.services import Sense
from sense.models.services import DrawFig

if TYPE_CHECKING:
    from sense.models import SensorFigure


class Sensor(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)

    sense_class: Type[Sense]
    fig_class: Type[DrawFig]

    def __str__(self):
        concrete = self.concrete_instance
        base_name = getattr(concrete._meta, "verbose_name", Sensor._meta.verbose_name)
        return base_name + concrete.name

    def sense(self) -> Optional[Sense.SenseData]:
        return self.sense_class(self).sense()

    @property
    def try_light_intensity(self):
        from sense.models import LightIntensitySensor

        if isinstance(self, LightIntensitySensor):
            return self
        try:
            return self.lightintensitysensor
        except:
            return None

    @property
    def try_soil_moisture(self):
        from sense.models import SoilMoistureSensor

        if isinstance(self, SoilMoistureSensor):
            return self
        try:
            return self.soilmoisturesensor
        except:
            return None

    @property
    def try_temperature_humidity(self):
        from sense.models import TemperatureHumiditySensor

        if isinstance(self, TemperatureHumiditySensor):
            return self
        try:
            return self.temperaturehumiditysensor
        except:
            return None

    @property
    def try_ultrasonic(self):
        from sense.models import UltrasonicSensor

        if isinstance(self, UltrasonicSensor):
            return self
        try:
            return self.ultrasonicsensor
        except:
            return None

    @property
    def concrete_instance(self):
        return (
            self.try_light_intensity
            or self.try_soil_moisture
            or self.try_temperature_humidity
            or self.try_ultrasonic
        )

    def get_figure(self) -> "SensorFigure":
        try:
            return self.figure
        except:
            from sense.models import SensorFigure

            return SensorFigure.objects.create(sensor=self, file=None)

    def update_figure(self) -> None:
        figure = self.get_figure()
        plot_file = self.fig_class(self).draw_fig()
        if plot_file:
            django_file = File(plot_file)
            figure.set_new_file(django_file)

    class Meta:
        verbose_name = "سنسور"
        verbose_name_plural = "سنسورها"
