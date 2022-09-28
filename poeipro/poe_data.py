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

    def __post_init__(self):
        self.time = self.update_time()

    def update_time(self):
        return time()

    def to_tupple(self):
        return ("{}_{}".format(self.ip, self.id), SensorType(self.type).name, self.reading, self.time)
