from enum import Enum


class Constants(Enum):
    # Isolated
    ISOLATED: bool = True

    # Protocol API
    API_URL: str = "https://brokenprotocol.xyz"
    ENDPOINT_AUTH_LOGIN: str = "/Authentication/Login"
    ENDPOINT_DEVICE_HEARTBEAT: str = "/Device/Heartbeat"
    ENDPOINT_DEVICE_CANPICKUP: str = "/Device/CanPickup"
    ENDPOINT_DEVICE_PICKEDUPOBJECT: str = "/Device/PickedUpObject"
    ENDPOINT_DEVICE_PUTBACKOBJECT: str = "/Device/PutBackObject"
    ENDPOINT_DETERMINED_OBJECT: str = "/Device/DeterminedObject"
    ENDPOINT_DEVICE_LOG: str = "/Device/Log"
    ENDPOINT_DEVICE_SENSORDATA: str = "/Device/SensorData"

    # Brightness values
    LIGHT_GATE_VALUE: int = 500
    WHITE_RANGE_START: int = 150
    WHITE_RANGE_END: int = 300
    BLACK_RANGE_START: int = 30
    BLACK_RANGE_END: int = 100

    # Timings
    MAIN_SWITCH_DEBOUNCE_MS: int = 200
    ROBOT_SWITCH_DEBOUNCE_MS: int = 200
    VIB_SENSOR_DEBOUNCE_MS: int = 150
    VIB_SENSOR_CHECK_COUNT: int = 20
    GATE_SENSOR_SENSE_INTERVAL_S: float = 0.05
    GATE_TO_COLOR_INTERVAL_S: float = 0.2
    COLOR_TO_ROBOT_INTERVAL_S: float = 0.3

    # Electronics
    ROBOT_MOTOR_FORWARD_PIN: int = 9
    ROBOT_MOTOR_BACKWARD_PIN: int = 11
    ROBOT_MOTOR_ENABLE_PIN: int = 10
    ROBOT_MOTOR_VIBRATION_PIN: int = 2
    ROBOT_MOTOR_POWER: int = 100
    ROBOT_ARRIVAL_SWITCH_PIN: int = 13
    ROBOT_START_SWITCH_PIN: int = 19
    SORTING_BELT_MOTOR_FORWARD_PIN: int = 16
    SORTING_BELT_MOTOR_BACKWARD_PIN: int = 20
    SORTING_BELT_MOTOR_ENABLE_PIN: int = 21
    SORTING_BELT_VIBRATION_PIN: int = 4
    SORTING_BELT_MOTOR_POWER: int = 100
    MAIN_BELT_MOTOR_FORWARD_PIN: int = 25
    MAIN_BELT_MOTOR_BACKWARD_PIN: int = 8
    MAIN_BELT_MOTOR_ENABLE_PIN: int = 12
    MAIN_BELT_MOTOR_POWER: int = 70
    PHOTOTRANSISTOR_CLK_PIN: int = 14
    PHOTOTRANSISTOR_DOUT_PIN: int = 15
    PHOTOTRANSISTOR_DIN_PIN: int = 18
    PHOTOTRANSISTOR_CS_PIN: int = 23
    GATE_LIGHT_PIN: int = 26
    COLOR_LIGHT_PIN: int = 27
    MAIN_SWITCH_PIN: int = 22

    # Object detection
    OBJECT_DETECTION_ENABLED: bool = True
    OBJECT_DETECTION_MODEL: str = "object_detection/model.tflite"
    OBJECT_DETECTION_WHITE_THRESHOLD: float = 0.9
    OBJECT_DETECTION_BLACK_THRESHOLD: float = 0.9
    OBJECT_DETECTION_NONE_THRESHOLD: float = 0.2
