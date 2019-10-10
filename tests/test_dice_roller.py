import unittest

from utils.dice_roller import roll_die


class TestDiceRoller(unittest.TestCase):
    def test_boundaries_roll_20(self):
        for i in range(100):
            a = roll_die(20)
            assert(a > 0)
            assert(a < 21)
