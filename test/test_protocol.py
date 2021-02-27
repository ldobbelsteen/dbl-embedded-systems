from src import protocol
#from src import constants


class TestProtocol:
    __protocol = protocol.Protocol

    def test_login(self):
        result = self.__protocol.login(self)
        print(result)
        assert (result is not None) and (result != "")

    ## these methods are private, how to test them? We need to make it public I think.
    # def test_get_request(self):
    #     result = self.__protocol.__get
    #     print(result)
    #     assert result == 1

    # def test_get_request_with_header(self):
    #     result = self.__photo.get_color(358.91)
    #     print(result)
    #     assert result == 1
    
    # def test_get_request_empty_token_with_header_bool_token_true(self):
    #     result = self.__photo.get_color(358.91)
    #     print(result)
    #     assert result == 1
    
    # def test_get_request_with_bool_token_true(self):
    #     result = self.__photo.get_color(358.91)
    #     print(result)
    #     assert result == 1

    # def test_get_request_with_bool_token_false(self):
    #     result = self.__photo.get_color(358.91)
    #     print(result)
    #     assert result == 1

