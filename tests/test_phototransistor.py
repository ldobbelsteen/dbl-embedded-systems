import unittest

from src import phototransistor


class TestSum(unittest.TestCase):
    __photo = phototransistor.Phototransistor

    def test_list_black(self):
        """
        Test that it gives white by white insertion of brightness.
        """
        result = self.__photo.get_color(358.5)
        self.assertEqual(result, 1)

    def test_list_white(self):
        """
        Test that it gives black by insertion of black percentage brightness.
        """
        result = self.__photo.get_color(358.3)
        self.assertEqual(result, 0)

    def test_list_white(self):
        """
        Test that it gives none by insertion of brightness mediate.
        """
        result = self.__photo.get_color(358.4)
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
