import requests
import json
import time
import logger
from constants import Constants


class Protocol:
    __token = None
    __logger = None

    def __init__(self):
        self.__logger = logger.Logger(self)

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
            response = requests.get(Constants.API_URL.value + endpoint, headers=headers)
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
            response = requests.post(Constants.API_URL.value + endpoint, data=json.dumps(data), headers=headers)
            if self.__check_response_status(response.status_code):
                break
            tries = tries + 1
            time.sleep(0.5)

        dictResp = json.loads(response.text)
        # todo-> Check status code before returning (error handling) 200 good, but when it returns lik 400 then it is
        #  error.
        return dictResp

    def login(self):
        headers = {'Content-Type': 'application/json'}
        data = {'User': 'group4', 'Password': 'HNTS79MA0E'}
        dictResp = self.__post_request(Constants.ENDPOINT_AUTH_LOGIN.value, headers, data, False)
        self.__token = str(dictResp['Token'])
        self.__logger.log(["Success", "Token"], "The following Token is stored:\n" + self.__token)

    def heartbeat(self):
        if self.__token is not None:
            self.__get_request(Constants.ENDPOINT_DEVICE_HEARTBEAT.value, {}, True, False)
            self.__logger.log(["Success", "Heartbeat"], "API Successfully Responded Heartbeat.")
            # check if succes code 200 is return or not. Or maybe checking inside __post_request (errror handler).

    def can_pickup(self):
        if self.__token is not None:
            dictResp = self.__get_request(Constants.ENDPOINT_DEVICE_CANPICKUP.value)
            # check if succes code 200 is return or not. Or maybe checking inside __post_request (errror handler).
            self.__logger.log(["Success", "Can_Pickup"], "API Successfully Responded Can_Pickup:\n" + str(dictResp))
            return dictResp

    def picked_up_object(self):
        if self.__token is not None:
            dictResp = self.__post_request(Constants.ENDPOINT_DEVICE_PICKEDUPOBJECT.value)
            self.__logger.log(["Success", "Picked_Up_Object"], "API Successfully Responded Picked_Up_Object:\n" + str(dictResp))
            return dictResp

    def put_back_object(self):
        if self.__token is not None:
            dictResp = self.__post_request(Constants.ENDPOINT_DEVICE_PUTBACKOBJECT.value)
            self.__logger.log(["Success", "Put_Back_Object"], "API Successfully Responded Put_Back_Object:\n" + str(dictResp))
            return dictResp

    def determined_object(self, color: int):
        if self.__token is not None:
            headers = {'Content-Type': 'application/json'}
            data = {'Color': color}
            dictResp = self.__post_request(Constants.ENDPOINT_DETERMINED_OBJECT.value, headers, data)
            # check if succes code 200 is return or not. Or maybe checking inside __post_request (errror handler).
            self.__logger.log(["Success", "Determined_Object"], "API Successfully Responded Determined_Object:\n" + str(dictResp))
            return dictResp

    def log(self, tags: list, message: str):
        if self.__token is not None:
            headers = {'Content-Type': 'application/json'}
            data = {'Tags': tags, 'Message': message}
            dictResp = self.__post_request(Constants.ENDPOINT_DEVICE_LOG.value, headers, data)
            # check if succes code 200 is return or not. Or maybe checking inside __post_request (errror handler).
            return dictResp

    def sensor_data(self, data: dict):
        if self.__token is not None:
            headers = {'Content-Type': 'application/json'}
            data = {'Data': data}
            dictResp = self.__post_request(Constants.ENDPOINT_DEVICE_SENSORDATA.value, headers, data)
            # check if succes code 200 is return or not. Or maybe checking inside __post_request (errror handler).
            self.__logger.log(["Success", "Sensor_Data"], "API Successfully Responded Sensor_Data:\n" + str(dictResp))
            return dictResp


if __name__ == '__main__':
    protocol = Protocol()
    protocol.login()
    protocol.heartbeat()
    protocol.can_pickup()
    protocol.picked_up_object()
    protocol.put_back_object()
    protocol.determined_object(0)
    protocol.log(["test"], "This is a test message")
    protocol.sensor_data({'test': 'test_data'})
    