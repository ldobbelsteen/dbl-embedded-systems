import requests
import json
from constants import Constants


class Protocol:
    __token = None

    def login(self):
        headers = {'Content-Type': 'application/json'}
        data = {'User': 'Username', 'Password': 'Password'}
        response = requests.post(Constants.ENDPOINT + "/Authentication/Login", data=data, headers=headers)
        dictResp = json.loads(response.text)
        self.__token = str(dictResp['Token'])

    def heartbeat(self):
        if self.__token is not None:
            headers = {'auth': self.__token}
            requests.get(Constants.ENDPOINT + "/Device/Heartbeat", headers=headers)

    def can_pickup(self):
        if self.__token is not None:
            headers = {'auth': self.__token}
            response = requests.get(Constants.ENDPOINT + "/Device/CanPickup", headers=headers)
            dictResp = json.loads(response.text)
            return dictResp['Resp']

    def picked_up_object(self):
        if self.__token is not None:
            headers = {'auth': self.__token}
            response = requests.post(Constants.ENDPOINT + "/Device/PickedUpObject", headers=headers)
            dictResp = json.loads(response.text)
            return dictResp['Resp']

    def put_back_object(self):
        if self.__token is not None:
            headers = {'auth': self.__token}
            response = requests.post(Constants.ENDPOINT + "/Device/PutBackObject", headers=headers)
            dictResp = json.loads(response.text)
            return dictResp['Resp']

    def determined_object(self, color: int):
        if self.__token is not None:
            headers = {'Content-Type': 'application/json', 'auth': self.__token}
            data = {'Color': color}
            requests.post(Constants.ENDPOINT + "/Device/DeterminedObject", data=data, headers=headers)

    def log(self, tags: list, message: str):
        if self.__token is not None:
            headers = {'Content-Type': 'application/json', 'auth': self.__token}
            data = {'Tags': tags, 'Message': message}
            requests.post(Constants.ENDPOINT + "/Device/Log", data=data, headers=headers)

    def sensor_data(self, data: dict):
        if self.__token is not None:
            headers = {'Content-Type': 'application/json', 'auth': self.__token}
            data = {'Data': data}
            requests.post(Constants.ENDPOINT + "/Device/SensorData", data=data, headers=headers)
