from enum import Enum

class Opts(Enum):
    INITIALIZATION = 0
    POST = 1

class SensorType(Enum):
    FIRE = 0
    SMOKE = 1
    MOTION = 2
    HUMIDITY = 3
    TEMPERATURE = 4
    WATER = 5

class TC:  # Terminal Color
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'