import unittest

from utils.utilities import get_modifier


class TestGetModifier(unittest.TestCase):
    def test_modifiers(self):
        """
            Tests that modifiers are correctly calculated
            :return: nothing
        """
        a = get_modifier(1)
        assert(a == -5)

        a = get_modifier(2)
        assert(a == -4)
        a = get_modifier(3)
        assert(a == -4)

        a = get_modifier(4)
        assert(a == -3)
        a = get_modifier(5)
        assert(a == -3)

        a = get_modifier(6)
        assert(a == -2)
        a = get_modifier(7)
        assert(a == -2)

        a = get_modifier(8)
        assert(a == -1)
        a = get_modifier(9)
        assert(a == -1)

        a = get_modifier(10)
        assert(a == 0)
        a = get_modifier(11)
        assert(a == 0)

        a = get_modifier(12)
        assert(a == 1)
        a = get_modifier(13)
        assert(a == 1)

        a = get_modifier(14)
        assert(a == 2)
        a = get_modifier(15)
        assert(a == 2)

        a = get_modifier(16)
        assert(a == 3)
        a = get_modifier(17)
        assert(a == 3)

        a = get_modifier(18)
        assert(a == 4)
        a = get_modifier(19)
        assert(a == 4)

        a = get_modifier(20)
        assert(a == 5)
        a = get_modifier(21)
        assert(a == 5)

        a = get_modifier(22)
        assert(a == 6)
        a = get_modifier(23)
        assert(a == 6)

        a = get_modifier(24)
        assert(a == 7)
        a = get_modifier(25)
        assert(a == 7)

        a = get_modifier(26)
        assert(a == 8)
        a = get_modifier(27)
        assert(a == 8)

        a = get_modifier(28)
        assert(a == 9)
        a = get_modifier(29)
        assert(a == 9)

        a = get_modifier(30)
        assert(a == 10)
