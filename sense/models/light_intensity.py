
from sense.models import Sensor
from sense.models.services import SenseLightIntensity


class LightIntensitySensor(Sensor):

    sense_class = SenseLightIntensity

    class Meta:
        verbose_name = 'سنسور شدت نور'
        verbose_name = 'سنسور‌های شدت نور'
