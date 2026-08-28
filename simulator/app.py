import time
from prometheus_client import start_http_server, Gauge
import random
temperature = Gauge('room_temperature_celsius', 'Room temperature in Celsius')

start_http_server(8000)

print("Metrics available at http://localhost:8000/metrics")

current_temperature = 23.5

while True:
    current_temperature += random.uniform(-0.3, 0.3)
    current_temperature = max(18.0, min(35.0, current_temperature))

    temperature.set(round(current_temperature, 2))

    time.sleep(1)
