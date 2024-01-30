from django.db import models


class SensorFigure(models.Model):
    sensor = models.OneToOneField(
        to="sense.Sensor",
        related_name="figure",
        on_delete=models.CASCADE,
        verbose_name="سنسور مربوطه",
    )

    file = models.FileField(verbose_name="فایل نمودار", null=True, blank=True)

    class Meta:
        verbose_name = "نمودار سنسور"
        verbose_name_plural = "نمودارهای سنسور"
