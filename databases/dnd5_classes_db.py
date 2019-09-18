import json
import os
import sqlite3

from dnd5_character.DnD5Class import DnD5Class
from utils.utilities import list_to_str

CLASS_DATA_DIR = 'databases/data/classes/'

CREATE_CLASS_TABLE_REQUEST = '''CREATE TABLE IF NOT EXISTS dnd5_classes 
                                (id integer primary key, name text not null, hit_dice, weapon_proficiencies_to_add,
                                skill_proficiency_choices_number, skill_proficiency_choices_list, class_feature_names, 
                                class_feature_descriptions, class_feature_choices_names, class_feature_choices_lists, 
                                class_feature_choices_number, armor_proficiencies)'''

INSERT_CLASS_INTO_REQUEST = '''INSERT INTO dnd5_classes(name, hit_dice, weapon_proficiencies_to_add, 
                                class_feature_names, class_feature_descriptions, armor_proficiencies, 
                                skill_proficiency_choices_number, skill_proficiency_choices_list) 
                                values (?,?,?,?,?,?,?,?)'''

DROP_CLASS_TABLE_REQUEST = '''DROP TABLE IF EXISTS dnd5_classes'''


def insert_dnd5_classes():
    classes = get_all_classes_from_json()
    if len(classes) > 0:
        connection = sqlite3.connect('dnd5_db.db')
        connection.executemany(INSERT_CLASS_INTO_REQUEST, classes)
        connection.commit()
        connection.close()


def get_all_classes_from_json():
    classes = []
    for file in os.listdir(CLASS_DATA_DIR):
        file_path = CLASS_DATA_DIR + file
        if file_path.endswith(".json"):
            with open(file_path) as fd:
                json_data = json.load(fd)
                for dnd_class in json_data:
                    class_feature_names = ''
                    class_feature_descriptions = ''
                    for feature in dnd_class["class_features"]:
                        class_feature_names += feature["name"] + ';'
                        class_feature_descriptions += feature["description"] + ';'
                    # remove last comma
                    class_feature_names = class_feature_names[:-1]
                    class_feature_descriptions = class_feature_descriptions[:-1]
                    element = (dnd_class["name"],
                               dnd_class["hit_dice"],
                               list_to_str(dnd_class["weapon_proficiencies_to_add"]),
                               class_feature_names,
                               class_feature_descriptions,
                               list_to_str(dnd_class["armor_proficiencies_to_add"]),
                               dnd_class["skill_proficiency_choices"]["number"],
                               list_to_str(dnd_class["skill_proficiency_choices"]["skill_list"])
                               )
                    classes.append(element)
    return classes


def look_for_class_by_name(name):
    if name != "":
        connection = sqlite3.connect('dnd5_db.db')
        cursor = connection.cursor()
        select_request = '''SELECT * from dnd5_classes WHERE name = (?) '''
        cursor.execute(select_request, (name,))
        record = cursor.fetchone()
        dnd_class = change_record_into_class(record)
        connection.close()
        return dnd_class
    return None


def get_all_classes_names():
    names = []
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT name from dnd5_classes'''
    cursor.execute(select_request)
    records = cursor.fetchall()
    for i in records:
        names.append(i[0])
    return names


def change_record_into_class(record):
    if record is not None:
        dnd_class = DnD5Class("temp")
        dnd_class.name = record[1]
        dnd_class.hit_dice = record[2]
        if record[3] is not '':
            dnd_class.weapon_proficiencies_to_add = record[3].split(', ')
        if record[4] > 0:
            dnd_class.skill_proficiency_choices = {
                "number": record[4],
                "skill_proficiencies": record[5].split(', ')
            }

        class_feature_names = record[6].split(';')
        class_feature_descriptions = record[7].split(';')
        for i in range(len(class_feature_names)):
            class_feature = {
                "name": class_feature_names[i],
                "description": class_feature_descriptions[i]
            }
            dnd_class.class_features.append(class_feature)

        if record[11] is not '':
            dnd_class.armor_proficiencies_to_add = record[11].split(', ')
        return dnd_class
    return None

