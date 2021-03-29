import requests
import json
import time
import logger
from threading import Timer
from datetime import datetime
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
            Constants.ENDPOINT_AUTH_LOGIN.value, headers, data, False)
        self.__token = str(res['Token'])

    # Send heartbeat and keep doing so
    def heartbeat(self):
        self.__get_request(
            Constants.ENDPOINT_DEVICE_HEARTBEAT.value, {}, True, False)
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
        # check if success code 200 is returned or not. Or maybe checking inside __post_request (error handler)
        return res

    def __check_response_status(self, status_code: int):
        # here error handler
        # switch case (disctResp['statuscode'])
        # case 200: Succes
        # case 400: Return error to log (Terminal + API log)
        if status_code == 401:
            self.login()
        return True if status_code == 200 else False

    def __get_request(self, endpoint, headers: dict = {}, bool_token: bool = True, returned: bool = True):
        if bool_token and self.__token is not None:
            headers['auth'] = self.__token

        tries = 0
        while tries < 20:
            response = requests.get(
                Constants.API_URL.value + endpoint, headers=headers)
            if self.__check_response_status(response.status_code):
                break
            tries = tries + 1
            time.sleep(0.5)

        if returned:
            dictResp = json.loads(response.text)
            # todo-> Check status code before returning (error handling) 200 good, but when it returns lik 400 then it is
            #  error.
            return dictResp

    def __post_request(self, endpoint, headers: dict = {}, data: dict = {}, bool_token: bool = True):
        # Adding auth automatically in order to avoid repititve code, since token is always required by post except
        # one case.
        if bool_token and self.__token is not None:
            headers['auth'] = self.__token

        tries = 0
        while tries < 20:
            response = requests.post(
                Constants.API_URL.value + endpoint, data=json.dumps(data), headers=headers)
            if self.__check_response_status(response.status_code):
                break
            tries = tries + 1
            time.sleep(0.5)

        dictResp = json.loads(response.text)
        # todo-> Check status code before returning (error handling) 200 good, but when it returns lik 400 then it is
        #  error.
        return dictResp
