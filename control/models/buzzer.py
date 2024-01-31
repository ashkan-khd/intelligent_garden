import time
from django.conf import settings
from django.db import models



class Buzzer(models.Model):
    pin = models.IntegerField(verbose_name='شماره پین')

    def _buzz(self, pitch, duration):
        from RPi import GPIO
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)

        for i in range(cycles):
            GPIO.output(self.pin, True)
            time.sleep(delay)
            GPIO.output(self.pin, False)
            time.sleep(delay)


    def buzz(self, pitch, duration):
        if not settings.PRODUCTION:
            print('MOCK BUZZ!!')
            return

        from RPi import GPIO

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.pin, GPIO.OUT)
        try:
            self._buzz(pitch, duration)
        finally:
            GPIO.cleanup()

    def __str__(self) -> str:
        return f'هشداردهنده پین {self.pin}'

    class Meta:
        verbose_name = "هشداردهنده"
        verbose_name_plural = "هشداردهندگان"
