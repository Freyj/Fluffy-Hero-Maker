import json
from math import floor

from utils.dice_roller import keep_n_highest, sum_roll_dice


def is_valid_choice(item_list, item):
    """Checks that an item is in the list returns True if so"""
    for i in item_list:
        if item == i:
            return True
    return False


def list_to_str(table_choice):
    """Creates a string from a list of string and returns it"""
    choice_string = ""
    for i in table_choice:
        choice_string += str(i) + ", "
    # remove excess comma and space
    choice_string = choice_string[:-2]
    return choice_string


def list_to_str_with_number_and_line(table):
    """Creates a string from a list of strings and returns it
        with pretty printing and newlines already included"""
    table_string = ""
    for i in range(len(table)):
        number = i + 1
        table_string += str(number) + ": " + (str(table[i])) + "\n"
    table_string = table_string[:-2]
    return table_string


def dict_to_str(dictionary):
    """Creates a string from a dictionary to display"""
    result_str = ""
    if len(dictionary) > 0:
        for i in dictionary:
            result_str += str(i) + " : " + str(dictionary[i]) + "\n"
    return result_str


def dict_to_str_for_speed(dictionary):
    """Creates a string from a dictionary to display"""
    result_str = ""
    if len(dictionary) > 0:
        for i in dictionary:
            if dictionary[i] > 0:
                result_str += "\t" + str(i) + " : " + str(dictionary[i]) + "\n"
    return result_str


def generate_attributes(generation_type, stats=None):
    """Allows for more than one type of attributes generation
    Takes an int to pick the type of generation (example)
        1: 4d6 drop lowest
        2: 3d6
        3: 3d6 re-roll lower than 7 (8?)
        4: pick all 6
        5: re-roll if not 3 < bonus < 7"""
    attributes = {}
    random_attributes = []
    if generation_type == 1:
        for i in range(6):
            random_attributes.append(keep_n_highest(6, 4))
    if generation_type == 2:
        random_attributes = []
        for i in range(6):
            random_attributes.append(sum_roll_dice(6, 3))
    if generation_type == 3:
        random_attributes = []
        for i in range(6):
            roll_not_ok = True
            while roll_not_ok:
                roll = sum_roll_dice(6, 3)
                if roll > 7:
                    roll_not_ok = False
                    random_attributes.append(roll)
    if generation_type == 4:
        random_attributes = stats
    if generation_type == 5:
        valid_results = False
        while not valid_results:
            random_attributes = []
            for i in range(6):
                random_attributes.append(keep_n_highest(6, 4))
            valid_results = 3 <= sum_modifiers(random_attributes) <= 7

    if random_attributes:
        attributes = {
            "Strength": random_attributes[0],
            "Dexterity": random_attributes[1],
            "Constitution": random_attributes[2],
            "Intelligence": random_attributes[3],
            "Wisdom": random_attributes[4],
            "Charisma": random_attributes[5]
        }
    return attributes


def get_modifier(attribute):
    return floor((attribute - 10) / 2)


def sum_modifiers(stats):
    """Makes the sum of the various modifiers of stats to check the total bonuses"""
    mod_total = 0
    for item in stats:
        mod_total += get_modifier(item)
    return mod_total


def string_to_list_of_objects(objectstring):
    objects = objectstring.split('},')
    list_objects = []
    complete_object = {}
    for item in objects:
        complete_object["name"] = item[0]
        complete_object["description"] = item[1]
        list_objects.append(complete_object)
    return list_objects


def str_to_list(string_to_change):
    """Changes a string composed of items separated by , into a list"""
    item_list = []
    resulting_list = []
    if string_to_change is not None:
        item_list = string_to_change.split(',')
    for item in item_list:
        item = item.strip()
        resulting_list.append(item)
    return resulting_list


def attacks_string_to_display_string(attack_string):
    """Changes a string from
     [Bite;Melee;6;one creature;reach 5ft;10 (2d6 + 3) piercing damage;effect on hit];[....];[]
     to a displayable string of all available attacks"""
    resulting_string = ""
    attacks = attack_string.split(':')
    for attack in attacks:
        attack = attack[1:-1]
        attack_details = attack.split(';')
        resulting_string += "\n\t"+ attack_details[0] + " " + attack_details[1] + "\n"
        resulting_string += "\t\tHit Bonus: " + attack_details[2] + "\n\t\tTarget: " + attack_details[3]
        resulting_string += "\n\t\tDamage: " + attack_details[4]
        if attack_details[5] is not '':
            resulting_string += "\n\t\tOn Hit: " + attack_details[5]
    return resulting_string
