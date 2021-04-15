import random


def sum_roll_dice(die_type, dice_number):
    """" Rolls a number of dice of a die type and returns the sum"""
    resulting_sum = 0
    for _ in range(dice_number):
        resulting_sum += roll_die(die_type)
    return resulting_sum


def list_roll_dice(die_type, dice_number):
    """" Rolls a number of dice of a die type and returns the list of rolls"""
    resulting_list = []
    for _ in range(dice_number):
        resulting_list.append(roll_die(die_type))
    return resulting_list


def roll_die(die_type):
    """
    Roll a die of the die type
    :param die_type: int
    :return: a random int between 1 and die_type
    """
    result = random.randint(1, die_type)
    return result


def keep_n_highest_sum(die_type, dice_number):
    """" Rolls a number of dice of a die type and returns the sum
    of the n-1 highest dice"""
    full_roll = list_roll_dice(die_type, dice_number)
    full_roll.sort(reverse=True)
    full_roll.pop()
    resulting_sum = 0
    for _, roll in enumerate(full_roll):
        resulting_sum += roll
    return resulting_sum
