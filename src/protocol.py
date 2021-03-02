import requests
import json
from constants import Constants


class Protocol:
    __token = None

    def __check_response_status(self, dict_resp: dict):
        # here error handler
        # switch case (disctResp['statuscode'])
        # case 200: Succes
        # case 400: Return error to log (Terminal + API log)
        return True

    def __get_request(self, endpoint, headers: dict = {}, bool_token: bool = True):
        if bool_token and self.__token is not None:
            headers['auth'] = {'auth': self.__token}
        response = requests.get(Constants.API_URL.value + endpoint, headers=headers)
        dictResp = json.loads(response.text)
        # todo-> Check status code before returning (error handling) 200 good, but when it returns lik 400 then it is
        #  error.
        return dictResp

    def __post_request(self, endpoint, headers: dict = {}, data: dict = {}, bool_token: bool = True):
        # Adding auth automatically in order to avoid repititve code, since token is always required by post except
        # one case.
        if bool_token and self.__token is not None:
            headers['auth'] = {'auth': self.__token}
        response = requests.post(Constants.API_URL.value + endpoint, data=data, headers=headers)
        dictResp = json.loads(response.text)
        # todo-> Check status code before returning (error handling) 200 good, but when it returns lik 400 then it is
        #  error.
        return dictResp

    def login(self):
        headers = {'Content-Type': 'application/json'}
        data = {'User': 'Username', 'Password': 'Password'}
        dictResp = self.__post_request(Constants.ENDPOINT_AUTH_LOGIN.value, headers, data, False)
        self.__token = str(dictResp['Token'])

    def heartbeat(self):
        if self.__token is not None:
            dictResp = self.__get_request(Constants.ENDPOINT_DEVICE_HEARTBEAT.value)
            # check if succes code 200 is return or not. Or maybe checking inside __post_request (errror handler).

    def can_pickup(self):
        if self.__token is not None:
            dictResp = self.__get_request(Constants.ENDPOINT_DEVICE_CANPICKUP.value)
            # check if succes code 200 is return or not. Or maybe checking inside __post_request (errror handler).
            return dictResp['Resp']

    def picked_up_object(self):
        if self.__token is not None:
            dictResp = self.__post_request(Constants.ENDPOINT_DEVICE_PICKEDUPOBJECT.value)
            return dictResp['Resp']

    def put_back_object(self):
        if self.__token is not None:
            dictResp = self.__post_request(Constants.ENDPOINT_DEVICE_PUTBACKOBJECT.value)
            return dictResp['Resp']

    def determined_object(self, color: int):
        if self.__token is not None:
            headers = {'Content-Type': 'application/json'}
            data = {'Color': color}
            dictResp = self.__post_request(Constants.ENDPOINT_DETERMINED_OBJECT.value, headers, data)
            # check if succes code 200 is return or not. Or maybe checking inside __post_request (errror handler).

    def log(self, tags: list, message: str):
        if self.__token is not None:
            headers = {'Content-Type': 'application/json'}
            data = {'Tags': tags, 'Message': message}
            dictResp = self.__post_request(Constants.ENDPOINT_DEVICE_LOG.value, headers, data)
            # check if succes code 200 is return or not. Or maybe checking inside __post_request (errror handler).

    def sensor_data(self, data: dict):
        if self.__token is not None:
            headers = {'Content-Type': 'application/json'}
            data = {'Data': data}
            dictResp = self.__post_request(Constants.ENDPOINT_DEVICE_SENSORDATA.value, headers, data)
            # check if succes code 200 is return or not. Or maybe checking inside __post_request (errror handler).
