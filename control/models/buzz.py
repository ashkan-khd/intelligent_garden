import json
from django.db import models
from django.utils import timezone

class SensorBuzz(models.Model):
    on = models.BooleanField(default=True, verbose_name='روشن است؟')

    buzzer = models.ForeignKey(
        to="control.buzzer",
        related_name="buzzes",
        on_delete=models.CASCADE,
        verbose_name="هشداردهنده‌ی مربوطه",
    )

    sensor = models.ForeignKey(
        to="sense.Sensor",
        related_name="buzzes",
        on_delete=models.CASCADE,
        verbose_name="سنسور مربوطه",
    )

    pitch = models.IntegerField(verbose_name="اوج صدا")
    duration = models.IntegerField(verbose_name="طول صدا")

    for_how_long = models.DurationField(verbose_name="مدت زمان انتظار")

    sensor_result_filters = models.JSONField(verbose_name="فیلترهای روز نتیجه سنسور")
    
    last_effort = models.DateTimeField(null=True, blank=True)

    def try_buzz(self) -> bool:
        self.last_effort = timezone.now()
        self.save(update_fields=['last_effort'])

        
        qs = self.sensor.results.filter(created__gte=timezone.now()-self.for_how_long)
        if not qs.exists():
            return False

        if qs.count() != qs.filter(**self.sensor_result_filters).count():
            return False

        self.buzzer.buzz(self.pitch, self.duration)
        return True

    def __str__(self) -> str:
        return f'هشدار برای {str(self.sensor)} توسط {str(self.buzzer)}'
    class Meta:
        verbose_name = "هشدار سنسور"
        verbose_name_plural = "هشدارهای سنسور"
