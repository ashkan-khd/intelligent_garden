from sense.models import Sensor
from sense.models.services import SenseLightIntensity, DrawLightIntensityFig


class LightIntensitySensor(Sensor):
    sense_class = SenseLightIntensity
    fig_class = DrawLightIntensityFig

    class Meta:
        verbose_name = "سنسور شدت‌نور"
        verbose_name_plural = "سنسورهای شدت‌نور"
