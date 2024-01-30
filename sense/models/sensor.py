from typing import Optional, Type
from django.db import models

from sense.models.services import Sense


class Sensor(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)

    sense_class: Type[Sense]

    def __str__(self):
        base_name = getattr(self.Meta, "verbose_name", Sensor.Meta.verbose_name)
        return base_name + self.name

    def sense(self) -> Optional[Sense.SenseData]:
        return self.sense_class(self).sense()

    class Meta:
        verbose_name = "سنسور"
        verbose_name_plural = "سنسورها"
        abstract = True
