import json
import os
import sqlite3

from dnd5.DnD5Race import DnD5Race
from utils.utilities import str_to_list

RACE_DATA_DIR = 'databases/data/dnd5/races/'

# field numbers for memory
# 1: name
# 2: abilities_plus_two
# 3: abilities_plus_one,
# 4: languages_added,
# 5: bonus_languages,
# 6: skill_proficiencies_added,
# 7: walking_speed,
# 8: flying_speed,
# 9: burrowing_speed,
# 10: climbing_speed,
# 11: swimming_speed,
# 12: age_bracket,
# 13: racial_traits_names,
# 14: racial_traits_descriptions,
# 15: vision,
# 16: spells_to_add,
# 17: weapon_proficiencies_to_add,
# 18: tool_proficiencies_number,
# 19: tool_proficiencies_choices,
# 20: cantrip_choices_number
# 21: cantrip_choices,
# 22: size,
# 23: racial_trait_choices,
# 24: armor_proficiencies_to_add

CREATE_RACE_TABLE_REQUEST = '''CREATE TABLE IF NOT EXISTS dnd5_races (id integer primary key, name text, 
abilities_plus_two, abilities_plus_one, languages_added, bonus_languages, skill_proficiencies_added, walking_speed, 
flying_speed, burrowing_speed, climbing_speed, swimming_speed, age_bracket, racial_traits_names, 
racial_traits_descriptions, vision, spells_to_add, weapon_proficiencies_to_add, tool_proficiencies_number, 
tool_proficiencies_choices, cantrip_choices_number numeric, cantrip_choices, size, racial_trait_choices, 
armor_proficiencies_to_add)'''


INSERT_RACE_INTO_REQUEST = '''INSERT INTO dnd5_races (name, abilities_plus_two, abilities_plus_one, languages_added, 
bonus_languages, skill_proficiencies_added, walking_speed, flying_speed, burrowing_speed, climbing_speed, 
swimming_speed, age_bracket, racial_traits_names, racial_traits_descriptions, vision, spells_to_add, 
weapon_proficiencies_to_add, tool_proficiencies_number, tool_proficiencies_choices, cantrip_choices_number, 
cantrip_choices, size, racial_trait_choices, armor_proficiencies_to_add) values 
(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''

DROP_RACE_TABLE_REQUEST = '''DROP TABLE IF EXISTS dnd5_races'''


def get_all_races_names():
    """
        Returns all the races names from the database
        :return: a list of strings
    """
    names = []
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT name from dnd5_races'''
    cursor.execute(select_request)
    records = cursor.fetchall()
    for i in records:
        names.append(i[0])
    return names


def get_number_of_races_in_db():
    """
        Returns the number of races in the dnd5_races table
        :return: integer representing the number of races in the database
    """
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT count() from dnd5_races'''
    cursor.execute(select_request)
    number_of_rows = cursor.fetchone()[0]
    connection.close()
    return number_of_rows


def insert_dnd5_race():
    """
        Parses all the json files in the races folder
        and inserts all the races in the database
        :return: nothing
        TODO: exceptions instead of prints for errors
    """
    if get_number_of_races_in_db() == 0:
        races = get_all_races_from_json_directory()
        if len(races) > 0:
            connection = sqlite3.connect('dnd5_db.db')
            connection.executemany(INSERT_RACE_INTO_REQUEST, races)
            connection.commit()
            connection.close()
    else:
        print("Races already in database")


def get_all_races_from_json_directory():
    """
        Parses the races from json and creates tuples to fill the database from it
        :return: the races as a list of tuples
    """
    races = []
    for file in os.listdir(RACE_DATA_DIR):
        file_path = RACE_DATA_DIR + file
        if file_path.endswith(".json"):
            with open(file_path, encoding='utf-8') as fd:
                json_data = json.load(fd)
                for dnd_race in json_data:
                    racial_trait_names = []
                    racial_trait_descriptions = []
                    # deal with racial traits
                    for i in range(len(dnd_race["racial_traits"])):
                        racial_trait_names.append(dnd_race["racial_traits"][i]["name"])
                        # change , into ; in the strings to ease up stuff
                        racial_trait_descriptions.append(dnd_race["racial_traits"][i]["description"].replace(',', ';'))
                    # deal with racial traits choices
                    choices_list = dnd_race["racial_traits_choices"]
                    racial_trait_choices = ""
                    for choice in choices_list:
                        racial_trait_choices += choice["name"] + "%"
                        racial_trait_choices += choice["description"] + '#'
                        racial_trait_choices += choice["link"] + "?"
                        for j in choice["choice_list"]:
                            racial_trait_choices += j + "/"
                        racial_trait_choices = racial_trait_choices[:-1] + "&"
                    racial_trait_choices = racial_trait_choices[:-1]
                    element = (dnd_race["name"],
                               ", ".join(dnd_race["abilities_plus_one"]),
                               ", ".join(dnd_race["abilities_plus_two"]),
                               ", ".join(dnd_race["languages_added"]),
                               dnd_race["bonus_languages"],
                               ", ".join(dnd_race["skill_proficiencies_added"]),
                               dnd_race["speed"]["walking"],
                               dnd_race["speed"]["flying"],
                               dnd_race["speed"]["burrowing"],
                               dnd_race["speed"]["climbing"],
                               dnd_race["speed"]["swimming"],
                               dnd_race["age_bracket"],
                               ", ".join(racial_trait_names),
                               ", ".join(racial_trait_descriptions),
                               ", ".join(dnd_race["vision"]),
                               ", ".join(dnd_race["spells_to_add"]),
                               ", ".join(dnd_race["weapon_proficiencies_added"]),
                               dnd_race["tool_proficiency_choice_nb"],
                               ", ".join(dnd_race["tool_proficiency_choice_list"]),
                               dnd_race["cantrip_choice_nb"],
                               ", ".join(dnd_race["cantrip_choice_list"]),
                               dnd_race["size"],
                               racial_trait_choices,
                               ", ".join(dnd_race["armor_proficiencies_added"])
                               )
                    races.append(element)
    return races


def look_for_race_by_name(name):
    """
        Returns one race as a DnD5Race object from the corresponding data in the database according to
         the name
        :param name: str
        :return: a DnD5Race object
    """
    if name != "":
        connection = sqlite3.connect('dnd5_db.db')
        cursor = connection.cursor()
        select_request = '''SELECT * from dnd5_races WHERE name = (?) '''
        cursor.execute(select_request, (name,))
        record = cursor.fetchone()
        race = change_record_into_race(record)
        connection.close()
        return race
    return None


def change_record_into_race(record):
    """
        Changes a tuple of a dnd race record from database to a DnD5Race Object
        :param record: a tuple representing a dnd race
        :return: a DnD5Race object
    """
    if record is not None:
        race = DnD5Race("temp")
        race.name = record[1]
        race.abilities_plus_one = str_to_list(record[2])
        race.abilities_plus_two = str_to_list(record[3])
        if record[4] is not '':
            race.languages = str_to_list(record[4])
        race.bonus_languages = record[5]
        if record[6] is not '':
            skill_list = str_to_list(record[6])
            for skill in skill_list:
                race.skill_proficiencies.add(skill)
        race.speed = {
            "walking": record[7],
            "flying": record[8],
            "burrowing": record[9],
            "climbing": record[10],
            "swimming": record[11]
        }
        race.age_bracket = record[12].split(',')
        if record[13] is not '':
            racial_traits_names = str_to_list(record[13])
            racial_traits_descriptions = str_to_list(record[14])
            for i in range(len(racial_traits_names)):
                item = {
                    "name": racial_traits_names[i],
                    "description": racial_traits_descriptions[i]
                }
                race.racial_traits.append(item)
        if record[15] is not '':
            race.vision.append((record[15]))
        if record[16] is not '':
            race.spells_to_add.append(record[16])
        if record[17] is not '':
            weapon_proficiencies = str_to_list(record[17])
            for prof in weapon_proficiencies:
                race.weapon_proficiencies_to_add.append(prof)
        if record[18] > 0:
            tool_proficiencies_number = record[18]
            tool_proficiencies_choices = str_to_list(record[19])
            race.tool_proficiency_choices = {
                "number": tool_proficiencies_number,
                "tool_proficiency": tool_proficiencies_choices
            }
        if record[20] > 0:
            cantrip_choices_number = record[20]
            cantrip_choices = str_to_list(record[21])
            race.cantrips_choice = {
                "number": cantrip_choices_number,
                "cantrips": cantrip_choices
            }
        race.size = record[22]
        if record[23] != '':
            racial_traits_choices = record[23]
            race.racial_traits_to_choose = parse_racial_traits_choices(racial_traits_choices)
        if record[24] != '':
            race.armor_proficiencies = str_to_list(record[24])
        return race
    return None


def parse_racial_traits_choices(racial_traits_choices):
    """
        Parse a string representing racial traits choices as :
        Name%Description#Links?Choice1/ChoiceN&
        and returns the racial traits choices as the DnD5Race class needs
        :param racial_traits_choices: a string
        :return a dictionary of racial traits choices
        """
    result =  {
        "number": 0,
        "traits": []
    }
    choices = racial_traits_choices.split('&')
    for choice in choices:
        item = {}
        name_and_rest = choice.split('%')
        item["name"] = name_and_rest[0]
        description_and_rest = name_and_rest[1].split('#')
        item["description"] = description_and_rest[0]
        links_and_rest = description_and_rest[1].split('?')
        item["links"] = links_and_rest[0]
        item["list"] = links_and_rest[1].split('/')
        result["number"] += 1
        result["traits"].append(item)
    return result
