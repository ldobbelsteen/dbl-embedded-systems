import unittest

from phototransistor import get_reading


class TestSum(unittest.TestCase):
    def test_list_black(self):
        """
        Test that it gives white by white insertion of brightness.
        """
        result = get_reading(data)
        self.assertEqual(result, 1)

    def test_list_white(self):
        """
        Test that it gives black by insertion of black percentage brightness.
        """
        result = get_reading(data)
        self.assertEqual(result, 0)

    def test_list_white(self):
        """
        Test that it gives none by insertion of brightness mediate.
        """
        result = get_reading(self, channel: int)
        self.assertEqual(result, 0)



if __name__ == '__main__':
    unittest.main()