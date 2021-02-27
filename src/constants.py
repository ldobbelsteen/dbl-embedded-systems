from enum import Enum


class Constants(Enum):
    # Protocol API
    API_URL = "https://whateverEndPoint"
    ENDPOINT_AUTH_LOGIN = "/Authentication/Login"
    ENDPOINT_DEVICE_HEARTBEAT = "/Device/Heartbeat"
    ENDPOINT_DEVICE_CANPICKUP = "/Device/CanPickup"
    ENDPOINT_DEVICE_PICKEDUPOBJECT = "/Device/PickedUpObject"
    ENDPOINT_DEVICE_PUTBACKOBJECT = "/Device/PutBackObject"
    ENDPOINT_DETERMINED_OBJECT = "/Device/DeterminedObject"
    ENDPOINT_DEVICE_LOG = "/Device/Log"
    ENDPOINT_DEVICE_SENSORDATA = "/Device/SensorData"

    # Brightness values
    WHITE_VALUE: int = 35
    BLACK_VALUE: int = 15

    # Robot
    ROBOT_MOTOR_POWER: int = 75

    # Sorting belt
    SORTING_BELT_POWER: int = 80

    # Controller
