import json
import os
import sqlite3

from dnd5_character.DnD5Class import DnD5Class
from utils.utilities import list_to_str

CLASS_DATA_DIR = 'databases/data/classes/'

CREATE_CLASS_TABLE_REQUEST = '''CREATE TABLE IF NOT EXISTS dnd5_classes 
                                (id integer primary key, name text not null, hit_dice, weapon_proficiencies_to_add,
                                skill_proficiency_choices_number, skill_proficiency_choices_list, class_feature_names, 
                                class_feature_descriptions, armor_proficiencies,
                                tool_proficiencies, class_feature_choices_names, class_feature_choices_descriptions,
                                class_feature_choices_tables, saving_throws_proficiencies)'''

# 1: name
# 2: hit_dice
# 3: weapon_proficiencies_to_add
# 4: class_feature_names
# 5: class_feature_descriptions
# 6: armor_proficiencies
# 7: skill_proficiency_choices_number
# 8: skill_proficiency_choices_list
# 9: tool_proficiencies
# 10: class_feature_choices_names
# 11: class_feature_choices_descriptions
# 12: class_feature_choices_tables
INSERT_CLASS_INTO_REQUEST = '''INSERT INTO dnd5_classes(name, hit_dice, weapon_proficiencies_to_add, 
                                class_feature_names, class_feature_descriptions, armor_proficiencies, 
                                skill_proficiency_choices_number, skill_proficiency_choices_list, tool_proficiencies,
                                class_feature_choices_names, class_feature_choices_descriptions,
                                class_feature_choices_tables, saving_throws_proficiencies) 
                                values (?,?,?,?,?,?,?,?,?,?,?,?,?)'''

DROP_CLASS_TABLE_REQUEST = '''DROP TABLE IF EXISTS dnd5_classes'''


def get_number_of_classes_in_db():
    """Returns an integer of the number of classes in the database"""
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()

    select_request = '''SELECT count() from dnd5_classes'''
    cursor.execute(select_request)
    number_of_rows = cursor.fetchone()[0]
    connection.close()
    return number_of_rows


def insert_dnd5_classes():
    if get_number_of_classes_in_db() == 0:
        classes = get_all_classes_from_json()
        if len(classes) > 0:
            connection = sqlite3.connect('dnd5_db.db')
            connection.executemany(INSERT_CLASS_INTO_REQUEST, classes)
            connection.commit()
            connection.close()
        else:
            print("Json folder of classes is empty.")
    else:
        print("Classes already in Database")


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
                    class_feature_choices = dnd_class["class_feature_choices"]
                    class_feature_choices_names = ""
                    class_feature_choices_descriptions = ""
                    class_feature_choices_tables = ""
                    for feature in class_feature_choices:
                        class_feature_choices_names += feature["name"] + ';'
                        class_feature_choices_descriptions += feature["description"] + ';'
                        class_feature_choices_table = feature["choice_table"]
                        for choice in class_feature_choices_table:
                            name = choice["name"]
                            description = choice["description"]
                            class_feature_choices_tables += name + "/" + description + ";"
                        class_feature_choices_tables = class_feature_choices_tables[:-1] + "#"
                    class_feature_choices_names = class_feature_choices_names[:-1]
                    class_feature_choices_descriptions = class_feature_choices_descriptions[:-1]
                    class_feature_choices_tables = class_feature_choices_tables[:-1]
                    element = (dnd_class["name"],
                               dnd_class["hit_dice"],
                               list_to_str(dnd_class["weapon_proficiencies_to_add"]),
                               class_feature_names,
                               class_feature_descriptions,
                               list_to_str(dnd_class["armor_proficiencies_to_add"]),
                               dnd_class["skill_proficiency_choices"]["number"],
                               list_to_str(dnd_class["skill_proficiency_choices"]["skill_list"]),
                               list_to_str(dnd_class["tool_proficiencies_to_add"]),
                               class_feature_choices_names,
                               class_feature_choices_descriptions,
                               class_feature_choices_tables,
                               list_to_str(dnd_class["saving_throws_proficiencies"])
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
        print(record)
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

        if record[8] is not '':
            dnd_class.armor_proficiencies_to_add = record[8].split(', ')

        if record[9] is not '':
            dnd_class.tool_proficiencies_to_add = record[9].split(', ')

        if record[10] is not '':
            feature_choices_names = record[10].split(';')
            feature_choices_descriptions = record[11].split(';')
            feature_choices_lists = record[12].split('#')
            feature_choices_table = []
            for i in range(len(feature_choices_names)):
                table = feature_choices_lists[i].split(';')
                for item in table:
                    resulting_choices = item.split('/')
                    choice = {
                        "name": resulting_choices[0],
                        "description": resulting_choices[1]
                    }
                    feature_choices_table.append(choice)

                feat_choice = {
                    "name": feature_choices_names[i],
                    "description": feature_choices_descriptions[i],
                    "choice_table": feature_choices_table
                }
                dnd_class.class_feature_choices.append(feat_choice)
        dnd_class.saving_throws = record[13].split(', ')
        return dnd_class
    return None

