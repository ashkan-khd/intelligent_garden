import os
from django.core.files import File
from django.db import models


class SensorFigure(models.Model):
    sensor = models.OneToOneField(
        to="sense.Sensor",
        related_name="figure",
        on_delete=models.CASCADE,
        verbose_name="سنسور مربوطه",
    )

    file = models.FileField(verbose_name="فایل نمودار", null=True, blank=True)

    def set_new_file(self, file: File):
        if self.file and self.file.url:
            file_path = self.file.path
            if os.path.exists(file_path):
                os.remove(file_path)

        self.file.save(
            f"{self.__class__.__name__}.png",
            file,
        )
        self.save()

    class Meta:
        verbose_name = "نمودار سنسور"
        verbose_name_plural = "نمودارهای سنسور"
