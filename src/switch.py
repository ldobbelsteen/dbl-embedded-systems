import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


class Switch:
	__input_pin: int = -1

	def __init__(self, input_pin: int = -1):
		self.__loaded = input_pin > -1
		if self.__loaded:
			self.__input_pin = input_pin
			GPIO.setup(self.__input_pin, GPIO.IN)
	
	def pressed(self):
		return GPIO.input(self.__input_pin) == GPIO.HIGH
