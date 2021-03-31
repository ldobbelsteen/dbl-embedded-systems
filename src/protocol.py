import json
import time
import requests
from threading import Timer
from constants import Constants


class Protocol:
    __token = None
    __logger = None
    __pickup_next = None

    def __init__(self, logger):
        self.__logger = logger
        self.login()
        self.heartbeat()
        self.pickup_check()

    # Log in by getting a token
    def login(self):
        headers = {'Content-Type': 'application/json'}
        data = {'User': 'group4', 'Password': 'HNTS79MA0E'}
        res = self.__post_request(
            Constants.ENDPOINT_AUTH_LOGIN.value, headers, data)
        self.__token = str(res['Token'])
        self.__logger.log("API login success with token: " + self.__token)

    # Send heartbeat and keep doing so
    def heartbeat(self):
        self.__get_request(Constants.ENDPOINT_DEVICE_HEARTBEAT.value)
        Timer(4, self.heartbeat).start()

    # Keep checking if next disk can be picked up until it can
    def pickup_check(self):
        self.__pickup_next = self.__get_request(
            Constants.ENDPOINT_DEVICE_CANPICKUP.value)
        if not self.__pickup_next:
            Timer(1, self.pickup_check).start()

    # Check if disk can be picked up right now
    def can_pickup(self):
        return self.__pickup_next

    # Send that disk of color has been picked up
    def picked_up(self, color: int):
        self.__post_request(Constants.ENDPOINT_DEVICE_PICKEDUPOBJECT.value)
        headers = {'Content-Type': 'application/json'}
        data = {'Color': color}
        self.__post_request(
            Constants.ENDPOINT_DETERMINED_OBJECT.value, headers, data)
        self.__pickup_next = False
        self.pickup_check()

    # Send a log with tags to the protocol
    def log(self, message: str, tags: list):
        headers = {'Content-Type': 'application/json'}
        data = {'Tags': tags, 'Message': message}
        res = self.__post_request(
            Constants.ENDPOINT_DEVICE_LOG.value, headers, data)
        return res

    # Check HTTP response code for errors
    def __check_response_status(self, status_code: int):
        if status_code == 401:
            self.login()
        return status_code == 200

    # Send a GET request to the API
    def __get_request(self, endpoint, headers: dict = {}):
        headers["auth"] = self.__token

        tries = 0
        while tries < 20:
            res = requests.get(Constants.API_URL.value +
                               endpoint, headers=headers)
            if self.__check_response_status(res.status_code):
                break
            tries += 1
            time.sleep(0.2)
        
        try:
            return json.loads(res.text)
        except:
            return

    # Send a POST request to the API
    def __post_request(self, endpoint, headers: dict = {}, data: dict = {}):
        headers["auth"] = self.__token

        tries = 0
        while tries < 20:
            res = requests.post(Constants.API_URL.value +
                                endpoint, data=json.dumps(data), headers=headers)
            if self.__check_response_status(res.status_code):
                break
            tries += 1
            time.sleep(0.2)

        try:
            return json.loads(res.text)
        except:
            return
