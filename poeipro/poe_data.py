from .enums_structs import SensorType
from dataclasses import dataclass
from time import time

@dataclass
class sensor:
    '''Sensor data and associated information'''
    ip :        str     = ""
    port :      str     = ""
    id :        str     = ""
    type :      int     = 0
    reading :   int     = 0
    time :      float   = 0
    status :    str     = ""

    def __post_init__(self):
        self.time = self.update_time()
        self.status = self.get_status(self.type, self.reading)

    def update_time(self):
        return time()

    def to_tupple(self):
        return ("{}_{}".format(self.ip, self.id), SensorType(self.type).name, self.reading, self.time, self.status)

    def get_status(self, sensor_type, val):
        # Threadholds provided by the summer IPRO team.
        val = int(val)
        status = "undefined"

        if sensor_type == SensorType.FIRE.value:
            if val < 1:
                status = "critical"
            elif val > 0:
                status = "normal"
        elif sensor_type == SensorType.SMOKE.value:
            if val < 160:
                status = "normal"
            elif val < 200:
                status = "warning"
            elif val >= 200:
                status = "critical"
                #email_list.append("y")
        elif sensor_type == SensorType.MOTION.value:
            if val == 1:
                status = "critical"
            elif val == 0:
                status = "normal"
        elif sensor_type == SensorType.HUMIDITY.value:
            if val >= 80:
                status = "critical"
            elif val < 80:
                status = "normal"
        elif sensor_type == SensorType.TEMPERATURE.value:
            if val > 82:
                status = "critical"
            elif val <= 82:
                status = "normal"
        elif sensor_type == SensorType.WATER.value:
            status = "undefined"
        else:
            status = "undefined"

        return status

