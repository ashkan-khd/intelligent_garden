from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
import time
import typing

from django.conf import settings

if typing.TYPE_CHECKING:
    from sense.models import (
        Sensor,
        LightIntensitySensor,
        SoilMoistureSensor,
        TemperatureHumiditySensor,
        UltrasonicSensor,
    )


class Sense(ABC):
    @dataclass
    class SenseData(ABC):
        def to_dict(self) -> dict:
            return asdict(self)

        def to_json(self) -> str:
            import json

            return json.dumps(self.to_dict())

    def __init__(self, sensor: "Sensor") -> None:
        self.sensor = sensor

    @abstractmethod
    def _sense(self) -> typing.Optional["SenseData"]:
        pass

    def _handle_exception(self, e):
        try:
            raise e
        except KeyboardInterrupt:
            pass

    def _final_callback(self):
        pass

    def __fake_sense(self) -> "SenseData":
        @dataclass
        class FakeSenseData(self.SenseData):
            msg: str

        return FakeSenseData(msg="fake data")

    def sense(self) -> typing.Optional["SenseData"]:
        if not settings.PRODUCTION:
            return self.__fake_sense()

        try:
            print(f"{str(self.sensor)} starting to sense...")
            return self._sense()
        except Exception as e:
            self._handle_exception(e)
        finally:
            self._final_callback()
            print("sensing has finished.")


class SenseLightIntensity(Sense):
    sensor: "LightIntensitySensor"

    @dataclass
    class SenseData(Sense.SenseData):
        light_level: float

    def _sense(self) -> "SenseData":
        import board
        import busio
        import adafruit_bh1750

        i2c = busio.I2C(board.SCL, board.SDA)
        sensor = adafruit_bh1750.BH1750(i2c)
        return self.SenseData(light_level=sensor.lux)


class SenseSoilMoisture(Sense):
    sensor: "SoilMoistureSensor"

    @dataclass
    class SenseData(Sense.SenseData):
        analog_moisture_level: int
        digital_moisture_level: int

    def sense_gpio_pin(self, pin):
        from RPi import GPIO

        GPIO.setup(pin, GPIO.IN)
        return GPIO.input(pin)

    def _sense(self) -> "SenseData":
        # Read analog soil moisture level (0-1)
        analog_moisture_level = self.sense_gpio_pin(self.sensor.analog_pin)

        # Read digital soil moisture level (0 or 1)
        digital_moisture_level = self.sense_gpio_pin(self.sensor.digital_pin)

        return self.SenseData(analog_moisture_level, digital_moisture_level)

    def _final_callback(self):
        from RPi import GPIO

        GPIO.cleanup()


class SenseTemperatureHumidity(Sense):
    sensor: "TemperatureHumiditySensor"

    @dataclass
    class SenseData(Sense.SenseData):
        temperature: float
        humidity: float

    def _sense(self) -> typing.Optional["SenseData"]:
        import Adafruit_DHT

        # Specify the sensor type (DHT22 in this case)
        sensor = getattr(Adafruit_DHT, self.sensor.tp)

        # Specify the GPIO pin for the AM2302 sensor (adjust based on your wiring)
        am2302_pin = self.sensor.am2302_pin

        humidity, temperature = Adafruit_DHT.read_retry(sensor, am2302_pin)

        # Check if the reading was successful
        if humidity is not None and temperature is not None:
            return self.SenseData(temperature, humidity)
        else:
            print("Failed to retrieve data from AM2302 sensor")
        return None


class SenseWaterHeightPercentage(Sense):
    sensor: "UltrasonicSensor"

    @dataclass
    class SenseData(Sense.SenseData):
        water_height: float
        water_percentage: float

    def get_distance(self):
        from RPi import GPIO

        # Trigger the sensor by sending a 10 microsecond pulse

        GPIO.output(self.sensor.trig_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.sensor.trig_pin, GPIO.LOW)

        # Measure the duration of the pulse on the Echo pin
        pulse_start_time = time.time()
        while GPIO.input(self.sensor.echo_pin) == 0:
            pulse_start_time = time.time()

        pulse_end_time = time.time()
        while GPIO.input(self.sensor.echo_pin) == 1:
            pulse_end_time = time.time()

        # Calculate the distance based on the speed of sound (343 meters/second)
        pulse_duration = pulse_end_time - pulse_start_time
        distance = (pulse_duration * 34300) / 2  # Distance in centimeters
        return distance

    def _sense(self) -> typing.Optional["SenseData"]:
        from RPi import GPIO

        GPIO.setmode(GPIO.BCM)
        # Read distance from the HC-SR04 sensor
        distance = self.get_distance()

        # Calculate the water height as a percentage of the total height
        percentage = max(
            0,
            min(
                (self.sensor.total_height_cm - distance)
                / self.sensor.total_height_cm
                * 100,
                100,
            ),
        )
        return self.SenseData(distance, percentage)

    def _final_callback(self):
        from RPi import GPIO

        GPIO.cleanup()
