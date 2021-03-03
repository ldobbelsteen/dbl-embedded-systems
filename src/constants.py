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
    WHITE_VALUE: int = 35
    BLACK_VALUE: int = 15

    # Robot
    ROBOT_MOTOR_POWER: int = 75

    # Sorting belt
    SORTING_BELT_POWER: int = 80

    # Controller
    R_F_PIN: int = -1
    R_B_PIN: int = -1
    R_E_PIN: int = -1
    SB_F_PIN: int = -1
    SB_B_PIN: int = -1
    SB_E_PIN: int = -1
    PH_CLK_PIN: int = -1
    PH_DOUT_PIN: int = -1
    PH_DIN_PIN: int = -1
    PH_CS_PIN: int = -1
    LED_PIN: int = -1
