import unittest

from utils.dice_roller import roll_die


class TestMethods(unittest.TestCase):
    def test_boundaries_roll_20(self):
        for i in range(100):
            a = roll_die(20)
            self.assertTrue(a > 0)
            self.assertTrue(a < 21)
