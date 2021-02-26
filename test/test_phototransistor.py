from src import phototransistor


class TestPhototransistor:
    __photo = phototransistor.Phototransistor

    def test_get_color_black1(self):
        result = self.__photo.get_color(358.91)
        print(result)
        assert result == 1

    def test_get_color_black2(self):
        result = self.__photo.get_color(358)
        print(result)
        assert result == 1

    def test_get_color_white1(self):
        result = self.__photo.get_color(358.92)
        print(result)
        assert result == 0

    def test_get_color_white2(self):
        result = self.__photo.get_color(359)
        print(result)
        assert result == 0
