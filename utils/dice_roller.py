import random


def sum_roll_dice(die_type, dice_number):
    """" Rolls a number of dice of a die type and returns the sum"""
    resulting_sum = 0
    for i in range(dice_number):
        resulting_sum += roll_die(die_type)
    return resulting_sum


def list_roll_dice(die_type, dice_number):
    """" Rolls a number of dice of a die type and returns the list of rolls"""
    resulting_list = []
    for i in range(dice_number):
        resulting_list.append(roll_die(die_type))
    return resulting_list


def roll_die(die_type):
    """"Roll a die of a die type and returns the resulting integer"""
    result = random.randint(1, die_type)
    return result


def keep_n_highest(die_type, dice_number):
    """" Rolls a number of dice of a die type and returns the sum
    of the n-1 highest dice"""
    full_roll = list_roll_dice(die_type, dice_number)
    full_roll.sort(reverse=True)
    full_roll.pop()
    resulting_sum = 0
    for i in range(len(full_roll)):
        resulting_sum += full_roll[i]
    return resulting_sum
