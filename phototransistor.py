import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

class Phototransistor:
    __mcp = None
    __loaded = False

    def __init__(self, clk_pin: int = -1, dout_pin: int = -1, din_pin: int = -1, cs_pin: int = -1):
        self.__loaded = (clk_pin > -1 and dout_pin > -1 and din_pin > -1 and cs_pin > -1)
        if self.__loaded:
            self.__mcp = Adafruit_MCP3008.MCP3008(clk=clk_pin, cs=cs_pin, miso=dout_pin, mosi=din_pin)

    def get_reading(self, channel: int):
        if self.__loaded:
            value = self.__mcp.read_adc(channel)
            return self.__value_to_fraction(value)
        return -1

    def get_reading_difference(self, channel: int):
        if self.__loaded:
            value = self.__mcp.read_adc_difference(channel)
            return self.__value_to_fraction(value)
        return -1
    
    def __value_to_fraction(self, value: int):
        return round(value / 1024, 3)

    # Requires: making sure that there is constant a physical light on it, such that the brightness percentage is constant.
    # only returns the brightness
    def get_color(self, channel: int):
        if self.__loaded:
            value = self.__value_to_fraction(self.__mcp.read_adc(channel)) * 100
            return 0 if value > 35 else 1
        return -1
