from unittest import TestCase
from src import protocol
from src import logger


class TestProtocol(TestCase):
    __protocol = protocol.Protocol(logger.Logger())

    # Test case, login function protocol
    def test_login(self):
        try:
            self.__protocol.login()
            assert True
        except Exception:
            assert False

    # Test case, log function protocol
    def test_log(self):
        self.__protocol.login()
        assert (self.__protocol.log("Test", ['Test']))
