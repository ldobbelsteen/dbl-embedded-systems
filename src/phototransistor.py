import Adafruit_MCP3008
from constants import Constants


class Phototransistor:
    __mcp = None
    __loaded: bool = False

    def __init__(self, clk_pin: int = -1, dout_pin: int = -1, din_pin: int = -1, cs_pin: int = -1):
        self.__loaded = (clk_pin > -1 and dout_pin > -1 and din_pin > -1 and cs_pin > -1)
        if self.__loaded:
            self.__mcp = Adafruit_MCP3008.MCP3008(clk=clk_pin, cs=cs_pin, miso=dout_pin, mosi=din_pin)

    def get_reading(self, channel: int):
        if self.__loaded:
            value = self.__mcp.read_adc(channel)
            return value
        return -1

    def get_reading_difference(self, channel: int):
        if self.__loaded:
            value = self.__mcp.read_adc_difference(channel)
            return value
        return -1

    @staticmethod
    def __value_to_fraction(value: float):
        return round(value / 1024, 3)

    # Requires: making sure that there is constant a physical light on it, such that the brightness percentage is
    # constant. only returns the brightness
    # white = 1, black = 0 (protocol requirement)
    @staticmethod
    def get_color(reading: float):
        reading = Phototransistor.__value_to_fraction(reading) * 100
        return 0 if reading > Constants.WHITE_VALUE else 1
