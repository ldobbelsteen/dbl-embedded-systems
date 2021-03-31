from unittest import TestCase
from src import protocol
from src import logger


class TestProtocol(TestCase):
    __protocol = protocol.Protocol(logger.Logger())

    def test_login(self):
        try:
            self.__protocol.login()
            assert True
        except:
            assert False
        # finally:
        #     print("yes")

    def test_canPickup(self):
        self.__protocol.can_pickup()
