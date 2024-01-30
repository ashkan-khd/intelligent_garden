from django.contrib import admin
from django.contrib.admin import ModelAdmin

from sense.models import (
    LightIntensitySensor,
    SoilMoistureSensor,
    TemperatureHumiditySensor,
    UltrasonicSensor,
    Sensor,
)


class SensorAdmin(ModelAdmin):
    list_display = [
        "get_str",
    ]
    fields = [
        "get_str",
        "name",
    ]

    def get_str(self, instance: Sensor):
        return str(instance)

    get_str.short_description = "مشخصه"


@admin.register(LightIntensitySensor)
class LightIntensitySensorAdmin(SensorAdmin):
    pass


@admin.register(SoilMoistureSensor)
class SoilMoistureSensorAdmin(SensorAdmin):
    exclusive_fields = [
        "analog_pin",
        "digital_pin",
    ]
    list_display = [
        *SensorAdmin.list_display,
        *exclusive_fields,
    ]
    fields = [
        *SensorAdmin.fields,
        *exclusive_fields,
    ]


@admin.register(TemperatureHumiditySensor)
class TemperatureHumiditySensorAdmin(SensorAdmin):
    exclusive_fields = [
        "tp",
        "am2302_pin",
    ]
    list_display = [
        *SensorAdmin.list_display,
        *exclusive_fields,
    ]
    fields = [
        *SensorAdmin.fields,
        *exclusive_fields,
    ]


@admin.register(UltrasonicSensor)
class UltrasonicSensorAdmin(SensorAdmin):
    exclusive_fields = [
        "trig_pin",
        "echo_pin",
        "total_height_cm",
    ]
    list_display = [
        *SensorAdmin.list_display,
        *exclusive_fields,
    ]
    fields = [
        *SensorAdmin.fields,
        *exclusive_fields,
    ]
