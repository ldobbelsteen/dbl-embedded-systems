import requests
import json
import time
import logger
from threading import Timer
from constants import Constants


class Protocol:
    __logger = None
    __token = None
    __active = None
    __can_pickup = None

    def __init__(self, logger):
        self.__logger = logger
        self.__token = self.login()
        self.__active = False
        self.__can_pickup = False

    def login(self):
        headers = {'Content-Type': 'application/json'}
        data = {'User': 'group4', 'Password': 'HNTS79MA0E'}
        res = self.__post_request(
            Constants.ENDPOINT_AUTH_LOGIN.value, headers, data, False)
        return str(res['Token'])

    def start(self):
        if self.__active:
            # Update pick up status
            Timer(1, self.start).start()
            self.__can_pickup = self.__get_request(
                Constants.ENDPOINT_DEVICE_CANPICKUP.value)
        else:
            # Send heartbeat
            Timer(5, self.start).start()
            self.__get_request(
                Constants.ENDPOINT_DEVICE_HEARTBEAT.value, {}, True, False)

    def set_active(self, active: bool):
        self.__active = active

    def can_pickup(self):
        cp = self.__can_pickup
        if not cp:
            self.__logger.log("Pickup blocked by the API!")
        return cp

    def picked_up(self, color: int):
        self.__post_request(Constants.ENDPOINT_DEVICE_PICKEDUPOBJECT.value)
        headers = {'Content-Type': 'application/json'}
        data = {'Color': color}
        self.__post_request(
            Constants.ENDPOINT_DETERMINED_OBJECT.value, headers, data)

    def log(self, message: str, tags: list):
        headers = {'Content-Type': 'application/json'}
        data = {'Tags': tags, 'Message': message}
        res = self.__post_request(
            Constants.ENDPOINT_DEVICE_LOG.value, headers, data)
        # check if succes code 200 is return or not. Or maybe checking inside __post_request (error handler).
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
