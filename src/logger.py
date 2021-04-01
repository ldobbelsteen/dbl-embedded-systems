# log message printer in the terminal & sender to the API.
import datetime


class Logger:
    __protocol = None  # Protocol used for logging

    # Logs a message with certain tags
    def log(self, message: str, tags: list = None):
        if tags is None:
            tags = []
        logs = ''
        message = str(datetime.datetime.now()) + ": " + message
        if len(tags) > 0:
            tags = ['[' + tag + ']' for tag in tags]
            logs = " ".join(tags) + ': '
        logs = logs + message
        # print on terminal
        print(logs)
        if self.__protocol is not None:
            # send to API
            self.__protocol.log(message, tags)

    def set_protocol(self, prot):
        self.__protocol = prot
