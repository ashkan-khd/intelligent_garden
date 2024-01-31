from django.contrib import admin
from django.contrib.admin import ModelAdmin
from control.models import Buzzer, SensorBuzz
from monitor.models import SensorResult, SensorMonitor


# Register your models here.
@admin.register(Buzzer)
class BuzzerAdmin(ModelAdmin):
    list_display = [
        "get_name",
        "pin",
    ]
    fields = [
        *list_display,
    ]
    readonly_fields = ["get_name"]

    def get_name(self, instance: Buzzer):
        return str(instance)

    get_name.short_description = "نام"


@admin.register(SensorBuzz)
class SensorBuzzAdmin(ModelAdmin):
    list_display = [
        "get_name",
        "on",
        "buzzer",
        "sensor",
        "pitch",
        "duration",
        "for_how_long",
    ]
    fields = [
        *list_display,
        "sensor_result_filters",
        "last_effort",
    ]
    readonly_fields = ["get_name", "last_effort"]

    def get_name(self, instance: Buzzer):
        return str(instance)

    get_name.short_description = "نام"
