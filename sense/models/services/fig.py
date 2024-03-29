from abc import ABC, abstractmethod
from tracemalloc import start
from typing import TYPE_CHECKING, List, Optional
from django.db.models import QuerySet
from django.utils import timezone
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from io import BytesIO

if TYPE_CHECKING:
    from sense.models import (
        Sensor,
        LightIntensitySensor,
        SoilMoistureSensor,
        TemperatureHumiditySensor,
        UltrasonicSensor,
    )
    from monitor.models import SensorResult
    from sense.models.services import Sense


class DrawFig(ABC):
    def __init__(self, sensor: "Sensor") -> None:
        self.sensor = sensor

    def get_sensor_results(self) -> List["SensorResult"]:
        from monitor.models import SensorResult

        end_time = timezone.now()
        start_time = end_time - timezone.timedelta(hours=0.5)

        return list(
            SensorResult.objects.filter(
                created__gt=start_time, created__lte=end_time, sensor=self.sensor
            ).order_by("created")
        )

    def get_sense_data(self, sensor_result: "SensorResult") -> "Sense.SenseData":
        return self.sensor.sense_class.SenseData.from_dict(sensor_result.result)

    @abstractmethod
    def _draw_fig(self, data):
        pass

    def draw_fig(self) -> Optional[BytesIO]:
        data = self.get_sensor_results()
        if data:
            return self._draw_fig(data)
        return None


class DrawLightIntensityFig(DrawFig):
    sensor: "LightIntensitySensor"

    def _draw_fig(self, data):
        # Extracting data for plotting
        timestamps = [entry.created for entry in data]
        intensities = [self.get_sense_data(entry).light_level for entry in data]

        # Creating a figure and an axes
        fig, ax = plt.subplots(figsize=(8, 6))

        # Plot light intensity
        ax.plot(timestamps, intensities)
        ax.set_xlabel("Time")
        ax.set_ylabel("Light Intensity")
        ax.set_title("Light Intensity Over 30 mins")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
        ax.tick_params(axis='x', rotation=45)
        
        # Adjust layout
        fig.tight_layout()

        plot_file = BytesIO()
        fig.savefig(plot_file, format="png")
        plot_file.seek(0)

        return plot_file


class DrawSoilMoistureFig(DrawFig):
    sensor: "SoilMoistureSensor"

    def _draw_fig(self, data):
        # Extracting data for plotting
        timestamps = [entry.created for entry in data]
        is_dry_values = [self.get_sense_data(entry).digital_moisture_level for entry in data]

        # Creating a figure and an axes
        fig, ax = plt.subplots(figsize=(8, 6))

        # Plot soil moisture as a stair diagram
        ax.step(timestamps, is_dry_values, where="post")
        ax.set_xlabel("Time")
        ax.set_ylabel("Soil Moisture")
        ax.set_title("Soil Moisture Over 30 mins")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
        ax.tick_params(axis='x', rotation=45)
        ax.yaxis.set_ticks([0, 1])  # Adjust y-axis ticks for boolean values
        ax.yaxis.set_ticklabels(["Not Dry", "Dry"])  # Adjust y-axis labels for boolean values
        ax.set_ylim(-0.1, 1.1)  # Set y-axis limits to accommodate boolean values

        # Adjust layout
        fig.tight_layout()

        plot_file = BytesIO()
        fig.savefig(plot_file, format="png")
        plot_file.seek(0)

        return plot_file


class DrawUltrasonicFig(DrawFig):
    sensor: "UltrasonicSensor"

    def _draw_fig(self, data):
        # Extracting data for plotting
        timestamps = [entry.created for entry in data]
        intensities = [self.get_sense_data(entry).water_percentage for entry in data]

        # Creating a figure and an axes
        fig, ax = plt.subplots(figsize=(8, 6))

        # Plot water level
        ax.plot(timestamps, intensities)
        ax.set_xlabel("Time")
        ax.set_ylabel("Water Level")
        ax.set_title("Water Level Over 30 mins")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
        ax.tick_params(axis='x', rotation=45)

        # Adjust layout
        fig.tight_layout()

        plot_file = BytesIO()
        fig.savefig(plot_file, format="png")
        plot_file.seek(0)

        return plot_file


class DrawTemperatureHumidityFig(DrawFig):
    sensor: "TemperatureHumiditySensor"

    def _draw_fig(self, data):
        timestamps = [entry.created for entry in data]
        temperatures = [self.get_sense_data(entry).temperature for entry in data]
        humidities = [self.get_sense_data(entry).humidity for entry in data]

        # Creating a plot with two subplots (temperature and humidity)
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))

        # Plot temperature
        ax1.plot(timestamps, temperatures, label="Temperature", color="red")
        ax1.set_ylabel("Temperature (Celsius)")
        ax1.legend(loc="upper left")

        # Plot humidity
        ax2.plot(timestamps, humidities, label="Humidity", color="blue")
        ax2.set_ylabel("Humidity (%)")
        ax2.legend(loc="upper left")

        # # Format x-axis as datetime
        # ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

        # Adjust layout
        plt.xlabel("Time")
        plt.tight_layout()
        date_format = mdates.DateFormatter("%m-%d %H:%M")
        plt.gca().xaxis.set_major_formatter(date_format)

        plot_file = BytesIO()
        plt.savefig(plot_file, format="png")
        plot_file.seek(0)
        return plot_file
