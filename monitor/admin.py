from django.contrib import admin
from django.contrib.admin import ModelAdmin
from monitor.models import SensorResult, SensorMonitor


@admin.register(SensorResult)
class SensorResultAdmin(ModelAdmin):
    list_display = [
        "created",
        "sensor",
    ]
    fields = [
        *list_display,
        "result",
    ]
    readonly_fields = ["result", "created"]


@admin.register(SensorMonitor)
class SensorMonitorAdmin(ModelAdmin):
    list_display = [
        "sensor",
        "last_monitor",
        "time_between_sense",
    ]
    fields = [
        *list_display,
    ]
    readonly_fields = ["last_monitor"]
