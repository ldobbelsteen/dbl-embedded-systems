#log message printer in the terminal & sender to the API.
import protocol
import datetime


class Logger:
    __protocol = None

    def __init__(self, prot: protocol.Protocol):
        self.__protocol = prot

    def log(self, message: str):
        self.log([], message)

    def log(self, tags: list, message: str):
        logs = ''
        message = str(datetime.datetime.now()) + ": " + message
        if len(tags) > 0:
            tags = ['[' + tag + ']' for tag in tags]
            logs = " ".join(tags) + ': '
        logs = logs + message
        # print on terminal
        print(logs)
        # send to API
        self.__protocol.log(tags, message)
