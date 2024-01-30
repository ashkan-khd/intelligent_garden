from django.db import models


class SensorResult(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    sensor = models.ForeignKey(
        to="sense.Sensor",
        related_name="results",
        on_delete=models.CASCADE,
        verbose_name="سنسور مربوطه",
    )

    result = models.JSONField(
        verbose_name="نتیجه سنسور",
    )

    class Meta:
        verbose_name = "نتیجه سنسور"
        verbose_name_plural = "نتایج سنسورها"
