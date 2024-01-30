from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.http.request import HttpRequest

from sense.models import (
    SensorFigure,
    LightIntensitySensor,
    SoilMoistureSensor,
    TemperatureHumiditySensor,
    UltrasonicSensor,
    Sensor,
)
from utility.admin import create_image_response


class SensorAdmin(ModelAdmin):
    list_display = [
        "get_str",
    ]
    fields = [
        "get_str",
        "name",
    ]
    readonly_fields = ["get_str", "get_fig"]

    def get_fields(self, request: HttpRequest, instance: Sensor):
        fields = super().get_fields(request, instance)
        return [
            *fields,
            "get_fig",
        ]

    def get_str(self, instance: Sensor):
        return str(instance)

    get_str.short_description = "مشخصه"

    def get_fig(self, instance: Sensor):
        figure: SensorFigure = instance.get_updated_figure()
        if figure.file and figure.file.url:
            return create_image_response(
                figure.file,
                width=500,
                height=500,
            )
        return "-"

    get_fig.short_description = "نمودار مربوط به سنسور"


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
