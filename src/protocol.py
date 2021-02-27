import requests
import json
from constants import Constants


class Protocol:
    __token = None

    def __check_response_status(self, dictResp):
        #here error handler
        #switch case (disctResp['statuscode'])
        #case 200: Succes
        #case 400: Return error to log (Terminal + API log)
        return True

    def __get_request(self, endpoint, headers = {}, bool_token = True):
        if (bool_token and self.__token is not None):
            headers['auth'] = {'auth': self.__token}
        response = requests.get(Constants.API_URL + endpoint, headers=headers)
        dictResp = json.loads(response.text)
        # todo-> Check status code before returning (error handling) 200 good, but when it returns lik 400 then it is error.
        return dictResp

    def __post_request(self, endpoint, headers = {}, data = {}, bool_token = True):
        ## Adding auth automatically in order to avoid repititve code, since token is always required by post except one case.
        if (bool_token and self.__token is not None):
            headers['auth'] = {'auth': self.__token}
        response = requests.post(Constants.API_URL + endpoint, data=data, headers=headers)
        dictResp = json.loads(response.text)
        # todo-> Check status code before returning (error handling) 200 good, but when it returns lik 400 then it is error.
        return dictResp

    def login(self):
        headers = {'Content-Type': 'application/json'}
        data = {'User': 'Username', 'Password': 'Password'}
        dictResp = self.__post_request(Constants.ENDPOINT_AUTH_LOGIN, headers, data, False)
        self.__token = str(dictResp['Token'])

    def heartbeat(self):
        dictResp = self.__get_request(Constants.ENDPOINT_DEVICE_HEARTBEAT)
        ## check if succes code 200 is return or not. Or maybe checking inside __post_request (errror handler).

    def can_pickup(self):
        dictResp = self.__get_request(Constants.ENDPOINT_DEVICE_CANPICKUP)
        ## check if succes code 200 is return or not. Or maybe checking inside __post_request (errror handler).
        return dictResp['Resp']

    def picked_up_object(self):
        dictResp = self.__post_request(Constants.ENDPOINT_DEVICE_PICKEDUPOBJECT)
        return dictResp['Resp']

    def put_back_object(self):
        dictResp = self.__post_request(Constants.ENDPOINT_DEVICE_PUTBACKOBJECT)
        return dictResp['Resp']

    def determined_object(self, color: int):
        headers = {'Content-Type': 'application/json'}
        data = {'Color': color}
        dictResp = self.__post_request(Constants.ENDPOINT_DETERMINED_OBJECT, headers, data)
        ## check if succes code 200 is return or not. Or maybe checking inside __post_request (errror handler).

    def log(self, tags: list, message: str):
        headers = {'Content-Type': 'application/json'}
        data = {'Tags': tags, 'Message': message}
        dictResp = self.__post_request(Constants.ENDPOINT_DEVICE_LOG, headers, data)
        ## check if succes code 200 is return or not. Or maybe checking inside __post_request (errror handler).

    def sensor_data(self, data: dict):
        headers = {'Content-Type': 'application/json'}
        data = {'Data': data}
        dictResp = self.__post_request(Constants.ENDPOINT_DEVICE_SENSORDATA, headers, data)
        ## check if succes code 200 is return or not. Or maybe checking inside __post_request (errror handler).
