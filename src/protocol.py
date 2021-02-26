import requests
from constants import Constants


def login():
    pass


def heartbeat():
    pass


def can_pickup():
    request = requests.get(Constants.ENDPOINT + "/Device/CanPickup")


def picked_up_object():
    pass


def put_back_object():
    pass


def determined_object():
    pass


def log(tag: str, message: str):
    pass


def sensor_data(data):
    pass
