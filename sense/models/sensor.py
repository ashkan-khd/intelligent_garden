from typing import Optional, Type
from django.db import models

from sense.models.services import Sense


class Sensor(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)

    sense_class: Type[Sense]

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
        return self.try_light_intensity or self.try_soil_moisture or self.try_temperature_humidity or self.try_ultrasonic

    class Meta:
        verbose_name = "سنسور"
        verbose_name_plural = "سنسورها"
