import protocol


class Logger:
    __protocol = None

    def __init__(self, prot: protocol.Protocol):
        self.__protocol = prot

    def log(self, message: str):
        self.log([], message)

    def log(self, tags: list, message: str):
        logs = ''
        if len(tags) > 0:
            tags = ['[' + tag + ']' for tag in tags]
            logs = " ".join(tags) + ': '
        logs = logs + message
        print(logs)
        self.__protocol.log(tags, message)
