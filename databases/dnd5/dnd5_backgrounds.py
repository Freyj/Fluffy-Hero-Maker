import json
import os
import sqlite3

from dnd5_character.DnD5Background import DnD5Background

BACKGROUND_DATA_DIR = 'databases/data/backgrounds/'

CREATE_BACKGROUND_TABLE_REQUEST = '''CREATE TABLE IF NOT EXISTS dnd5_backgrounds 
                                (id integer primary key, name text not null, skill_proficiencies, bonus_languages 
                                numeric, equipment text, feature text, personality_traits, ideals, bonds, flaws, 
                                background_description, feature_description, feature_choice, feature_choice_table)'''

INSERT_BACKGROUND_INTO_REQUEST = '''INSERT INTO dnd5_backgrounds(name, skill_proficiencies, bonus_languages, equipment, 
                                feature, personality_traits, ideals, bonds, flaws, background_description,
                                feature_description, feature_choice, feature_choice_table) 
                                values (?,?,?,?,?,?,?,?,?,?,?,?,?)'''

DROP_BACKGROUND_TABLE_REQUEST = '''DROP TABLE IF EXISTS dnd5_backgrounds'''


def get_number_of_backgrounds_in_db():
    """
        Returns the number of backgrounds in the dnd5_backgrounds table
        :return: integer representing the number of backgrounds in the database
    """
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT count() from dnd5_backgrounds'''
    cursor.execute(select_request)
    number_of_rows = cursor.fetchone()[0]
    connection.close()
    return number_of_rows


def insert_dnd5_background():
    """
        Parses all the json files in the backgrounds folder
        and inserts all the backgrounds in the database
        :return: nothing
        TODO: exceptions instead of prints for errors
    """
    if get_number_of_backgrounds_in_db() == 0:
        backgrounds = get_all_backgrounds_from_json()
        if len(backgrounds) > 0:
            connection = sqlite3.connect('dnd5_db.db')
            connection.executemany(INSERT_BACKGROUND_INTO_REQUEST, backgrounds)
            connection.commit()
            connection.close()
        else:
            print("Json folder of backgrounds is empty.")
    else:
        print("Backgrounds already in Database")


def get_all_backgrounds_from_json():
    """
        Parses the backgrounds from json and creates tuples to fill the database from it
        :return: the backgrounds as a list of tuples
    """
    backgrounds = []
    for file in os.listdir(BACKGROUND_DATA_DIR):
        file_path = BACKGROUND_DATA_DIR + file
        if file_path.endswith(".json"):
            with open(file_path, encoding='utf-8') as fd:
                json_data = json.load(fd)
                for background in json_data:
                    element = (background["name"],
                               ", ".join(background["skill_proficiencies"]),
                               background["bonus_languages"],
                               background["equipment"],
                               background["feature"],
                               ", ".join(background["personality_traits"]),
                               ", ".join(background["ideals"]),
                               ", ".join(background["bonds"]),
                               ", ".join(background["flaws"]),
                               background["background_description"],
                               background["feature_description"],
                               background["feature_choice"],
                               ", ".join(background["feature_choice_table"]))
                    backgrounds.append(element)
    return backgrounds


def get_all_background_names():
    """
        Returns all the background names from the database
        :return: a list of strings
    """
    names = []
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT name from dnd5_backgrounds'''
    cursor.execute(select_request)
    records = cursor.fetchall()
    for i in records:
        names.append(i[0])
    return names


def get_background_by_name(background_name: str):
    """
        Returns one background as a DnD5Background object from the corresponding data in the database according to
         the name
        :param background_name: str
        :return: a DnD5Background object
    """
    background = DnD5Background("temp")
    if background_name != "":
        connection = sqlite3.connect('dnd5_db.db')
        cursor = connection.cursor()
        select_request = '''SELECT * from dnd5_backgrounds WHERE name = (?) '''
        cursor.execute(select_request, (background_name,))
        record = cursor.fetchone()
        if record is not None:
            background.name = record[1]
            background.skill_proficiencies = record[2].split(', ')
            background.bonus_languages = record[3]
            background.equipment = record[4].split(', ')
            background.feature = record[5]
            background.personality_traits = record[6].split('., ')
            background.ideals = record[7].split('., ')
            background.bonds = record[8].split('., ')
            background.flaws = record[9].split('., ')
            background.description = record[10]
            background.feature_description = record[11]
            if record[12] is not '':
                background.feature_choice = record[12]
                background.feature_choice_table = record[13].split('.,')
        connection.close()
        return background
    return None


