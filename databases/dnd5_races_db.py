import json
import os
import sqlite3

from dnd5_character.DnD5Race import DnD5Race
from utils.utilities import list_to_str, str_to_list

RACE_DATA_DIR = 'databases/data/races/'

CREATE_RACE_TABLE_REQUEST = '''CREATE TABLE IF NOT EXISTS dnd5_races (id integer primary key, name text, 
abilities_plus_two, abilities_plus_one, languages_added, bonus_languages, skill_proficiencies_added, walking_speed, 
flying_speed, burrowing_speed, climbing_speed, swimming_speed, age_bracket, racial_traits_names, 
racial_traits_descriptions, vision, spells_to_add, weapon_proficiencies_to_add, tool_proficiencies_number, 
tool_proficiencies_choices, cantrip_choices_number numeric, cantrip_choices, size, racial_traits_choices_lists, 
racial_traits_choices_names, racial_traits_choices_links, racial_traits_choices_descriptions, armor_proficiencies_to_add) '''


INSERT_RACE_INTO_REQUEST = '''INSERT INTO dnd5_races (name, abilities_plus_two, abilities_plus_one, languages_added, 
bonus_languages, skill_proficiencies_added, walking_speed, flying_speed, burrowing_speed, climbing_speed, 
swimming_speed, age_bracket, racial_traits_names, racial_traits_descriptions, vision, spells_to_add, 
weapon_proficiencies_to_add, tool_proficiencies_number, tool_proficiencies_choices, cantrip_choices_number, 
cantrip_choices, size, racial_traits_choices_lists, racial_traits_choices_names, racial_traits_choices_links, 
racial_traits_choices_descriptions, armor_proficiencies_to_add) values 
(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''

DROP_RACE_TABLE_REQUEST = '''DROP TABLE IF EXISTS dnd5_races'''


def get_all_races_names():
    """Get all the class names from the database"""
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
    """Returns an integer of the number of races in the database"""
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()

    select_request = '''SELECT count() from dnd5_races'''
    cursor.execute(select_request)
    number_of_rows = cursor.fetchone()[0]
    connection.close()
    return number_of_rows


def insert_dnd5_race():
    """Inserts all the races data from the json files"""
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
    """ Get all the races from the json files and outputs a table of tuples of them
    Recovers all the races in  the data/races/*.json files """
    races = []
    for file in os.listdir(RACE_DATA_DIR):
        file_path = RACE_DATA_DIR + file
        if file_path.endswith(".json"):
            with open(file_path) as fd:
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
                    racial_traits_choices_lists = []
                    racial_traits_choices_names = []
                    racial_traits_choices_links = []
                    racial_traits_choices_descriptions = []
                    for i in range(len(choices_list)):
                        choices_list[i]["description"].strip(';')
                        racial_traits_choices_descriptions.append(choices_list[i]["description"].replace(',', ';'))
                        choices_list[i]["name"].strip(';')
                        racial_traits_choices_names.append(choices_list[i]["name"].replace(',', ';'))
                        choices_list[i]["link"].strip(';')
                        racial_traits_choices_links.append(choices_list[i]["link"].replace(',', ';'))
                        racial_traits_choices_lists.append(choices_list[i]["choice_list"])

                    element = (dnd_race["name"],
                               list_to_str(dnd_race["abilities_plus_one"]),
                               list_to_str(dnd_race["abilities_plus_two"]),
                               list_to_str(dnd_race["languages_added"]),
                               dnd_race["bonus_languages"],
                               list_to_str(dnd_race["skill_proficiencies_added"]),
                               dnd_race["speed"]["walking"],
                               dnd_race["speed"]["flying"],
                               dnd_race["speed"]["burrowing"],
                               dnd_race["speed"]["climbing"],
                               dnd_race["speed"]["swimming"],
                               dnd_race["age_bracket"],
                               list_to_str(racial_trait_names),
                               list_to_str(racial_trait_descriptions),
                               list_to_str(dnd_race["vision"]),
                               list_to_str(dnd_race["spells_to_add"]),
                               list_to_str(dnd_race["weapon_proficiencies_added"]),
                               dnd_race["tool_proficiency_choice_nb"],
                               list_to_str(dnd_race["tool_proficiency_choice_list"]),
                               dnd_race["cantrip_choice_nb"],
                               list_to_str(dnd_race["cantrip_choice_list"]),
                               dnd_race["size"],
                               list_to_str(racial_traits_choices_lists),
                               list_to_str(racial_traits_choices_names),
                               list_to_str(racial_traits_choices_links),
                               list_to_str(racial_traits_choices_descriptions),
                               list_to_str(dnd_race["armor_proficiencies_added"])
                               )
                    races.append(element)
    return races


def look_for_race_by_name(name):
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
    # print(record)
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
        if record[23] is not '':
            racial_traits_choices_lists = str_to_list(record[23])
            racial_traits_choices_names = str_to_list(record[24])
            racial_traits_choices_links = str_to_list(record[25])
            racial_traits_choices_descriptions = str_to_list(record[26])
            for i in range(len(racial_traits_choices_names)):
                race.racial_traits_to_choose["number"] += 1
                race.racial_traits_to_choose["traits"].append(
                    {
                        "name": racial_traits_choices_names[i],
                        "description": racial_traits_choices_descriptions[i],
                        "links": racial_traits_choices_links[i],
                        "list": racial_traits_choices_lists[i]
                    }
                )
        if record[27] is not '':
            race.armor_proficiencies = str_to_list(record[27])
        return race
    return None

