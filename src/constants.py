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

    # Robot
    ROBOT_MOTOR_POWER: int = 100

    # Sorting belt
    SORTING_BELT_POWER: int = 100

    # Main belt
    MAIN_BELT_POWER: int = 60

    # Controller
    R_F_PIN: int = 9
    R_B_PIN: int = 11
    R_E_PIN: int = 10
    S_A_PIN: int = 13
    S_S_PIN: int = 19
    SB_F_PIN: int = 16
    SB_B_PIN: int = 20
    SB_E_PIN: int = 21
    MB_F_PIN: int = 25
    MB_B_PIN: int = 8
    MB_E_PIN: int = 12
    PH_CLK_PIN: int = 14
    PH_DOUT_PIN: int = 15
    PH_DIN_PIN: int = 18
    PH_CS_PIN: int = 23
    LED_G_PIN: int = 26
    LED_C_PIN: int = 27
    VIB_SENSORS_PINS: list = [17]
