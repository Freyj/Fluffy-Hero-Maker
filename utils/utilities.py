import json
from math import floor

from utils.dice_roller import keep_n_highest_sum, sum_roll_dice


def is_valid_choice(item_list, item):
    """Checks that an item is in the list returns True if so"""
    for i in item_list:
        if item == i:
            return True
    return False


def list_to_str_with_number_and_line(table):
    """Creates a string from a list of strings and returns it
        with pretty printing and newlines already included"""
    table_string = ""
    for count, string in enumerate(table):
        number = count + 1
        table_string += str(number) + ": " + (str(string)) + "\n"
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
        for _ in range(6):
            random_attributes.append(keep_n_highest_sum(6, 4))
    if generation_type == 2:
        random_attributes = []
        for _ in range(6):
            random_attributes.append(sum_roll_dice(6, 3))
    if generation_type == 3:
        random_attributes = []
        for _ in range(6):
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
            for _ in range(6):
                random_attributes.append(keep_n_highest_sum(6, 4))
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


class CTEncoder(json.JSONEncoder):
    """
        https://github.com/PyCQA/pylint/issues/414 for the #pylint: disable=E0202
    """
    def default(self, o):  # pylint: disable=E0202
        return o.__dict__
