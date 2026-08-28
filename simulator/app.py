import time
import random
from prometheus_client import Counter, Gauge, start_http_server

rooms = {
    "living_room": {
        "temperature": 22.5,
        "humidity": 45.0,
        "co2": 650.0,
        "offline_cycles": 0,
    },
    "bedroom": {
        "temperature": 21.0,
        "humidity": 50.0,
        "co2": 700.0,
        "offline_cycles": 0,
    },
    "office": {
        "temperature": 23.0,
        "humidity": 42.0,
        "co2": 800.0,
        "offline_cycles": 0,
    },
}
readings = Counter(
    "sensor_readings_total",
    "Total number of sensor readings",
    ["room"],
)

sensor_online = Gauge(
    "sensor_online",
    "Whether the room sensor is online",
    ["room"],
)

sensor_errors = Counter(
    "sensor_errors_total",
    "Total number of sensor errors",
    ["room"],
)


humidity = Gauge('room_humidity_percent', 'Room humidity in percent', ['room'])
co2 = Gauge('room_co2_ppm', 'Room CO2 in ppm', ['room'])
temperature = Gauge('room_temperature_celsius', 'Room temperature in Celsius', ['room'])

start_http_server(8000)

print("Metrics available at http://localhost:8000/metrics")

while True:
    for room_name, state in rooms.items():
        if state["offline_cycles"] == 0 and random.random() < 0.05:
            state["offline_cycles"] = 3
            sensor_errors.labels(room=room_name).inc()
        
        if state["offline_cycles"] > 0:
            sensor_online.labels(room=room_name).set(0)
            state["offline_cycles"] -= 1
            continue
        
        sensor_online.labels(room=room_name).set(1)
        state["temperature"] = max(
            18.0,
            min(30.0, state["temperature"] + random.uniform(-0.3, 0.3)),
        )

        state["humidity"] = max(
            30.0,
            min(70.0, state["humidity"] + random.uniform(-1.0, 1.0)),
        )
        state["co2"] = max(
            400.0,
            min(1600.0, state["co2"] + random.uniform(-20.0, 20.0)),
        )

        temperature.labels(room=room_name).set(
            round(state["temperature"], 2)
        )

        humidity.labels(room=room_name).set(
            round(state["humidity"], 2)
        )
        co2.labels(room=room_name).set(
            round(state["co2"], 2)
        )
        readings.labels(room=room_name).inc()
        
    time.sleep(5)
