from src import phototransistor


class TestPhototransistor:
    __photo = phototransistor.Phototransistor

    # Test case, black disk
    def test_get_color_black1(self):
        result = self.__photo.get_color(21)
        print(result)
        assert result == 0

    # Test case, black disk
    def test_get_color_black2(self):
        result = self.__photo.get_color(79)
        print(result)
        assert result == 0

    # Test case, white disk
    def test_get_color_white1(self):
        result = self.__photo.get_color(101)
        print(result)
        assert result == 1

    # Test case, white disk
    def test_get_color_white2(self):
        result = self.__photo.get_color(299)
        print(result)
        assert result == 1
