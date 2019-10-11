import json
import os
import sqlite3

from databases.dnd5_spell_db import get_all_spells_of_class_and_level
from dnd5_character.DnD5Class import DnD5Class

CLASS_DATA_DIR = 'databases/data/classes/'

CREATE_CLASS_TABLE_REQUEST = '''CREATE TABLE IF NOT EXISTS dnd5_classes 
                                (id integer primary key, name text not null, hit_dice, weapon_proficiencies_to_add,
                                skill_proficiency_choices, class_features, armor_proficiencies, tool_proficiencies, 
                                class_feature_choices, saving_throws_proficiencies, added_equipment, equipment_choices, 
                                cantrip_number, spell_class_list, spells_1_number, spells_1_slots, casting_ability)'''

# 1: name
# 2: hit_dice
# 3: weapon_proficiencies_to_add
# 4: skill_proficiency_choices
# 5: class_features
# 6: armor_proficiencies
# 7: tool_proficiencies
# 8: class_feature_choices
# 9: saving_throw_proficiencies
# 10: added_equipment
# 11: equipment_choices
# 12: cantrip number
# 13: spell class list
# 14: spells number lvl 1
# 15: spell slots of lvl 1
# 16: casting_ability

INSERT_CLASS_INTO_REQUEST = '''INSERT INTO dnd5_classes(name, hit_dice, weapon_proficiencies_to_add,  
                                skill_proficiency_choices, class_features, armor_proficiencies, tool_proficiencies,
                                class_feature_choices, saving_throws_proficiencies, added_equipment, equipment_choices, 
                                cantrip_number, spell_class_list, spells_1_number, spells_1_slots, casting_ability) 
                                values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

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
                    element = (dnd_class["name"],
                               dnd_class["hit_dice"],
                               ", ".join(dnd_class["weapon_proficiencies_to_add"]),
                               json.dumps(dnd_class["skill_proficiency_choices"]),
                               json.dumps(dnd_class["class_features"]),
                               ", ".join(dnd_class["armor_proficiencies_to_add"]),
                               ", ".join(dnd_class["tool_proficiencies_to_add"]),
                               json.dumps(dnd_class["class_feature_choices"]),
                               ", ".join(dnd_class["saving_throws_proficiencies"]),
                               ", ".join(dnd_class["added_equipment"]),
                               dnd_class["equipment_choice"],
                               dnd_class["cantrips_to_add"]["number"],
                               dnd_class["cantrips_to_add"]["class_list"],
                               dnd_class["spells_to_add"],
                               dnd_class["level_one_spell_slots"],
                               dnd_class["casting_ability"]
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
        if record[4] is not '':
            print(record[4])
            dnd_class.skill_proficiency_choices = json.loads(record[4])
            print(dnd_class.skill_proficiency_choices)
        dnd_class.class_features = json.loads(record[5])
        if record[6] is not '':
            dnd_class.armor_proficiencies_to_add = record[6].split(', ')
        if record[7] is not '':
            dnd_class.tool_proficiencies_to_add = record[7].split(', ')
        if record[8] is not '':
            dnd_class.class_feature_choices = json.loads(record[8])
        dnd_class.saving_throws = record[9].split(', ')
        dnd_class.added_equipment = record[10].split(', ')
        dnd_class.equipment_choice = record[11]
        if record[12] > 0:
            dnd_class.is_spellcaster = True
            dnd_class.cantrips_choice["number"] = record[12]
            dnd_class.spellcaster_class = record[13]
            dnd_class.cantrips_choice["cantrips"] = get_all_spells_of_class_and_level(record[13], 0)
            if record[12] == 0:
                # Divine classes do not learn a fixed number of spells outside of cantrips
                dnd_class.is_divine_spellcaster = True
        if record[14] > 0:
            dnd_class.level_one_choice["number"] = record[14]
            dnd_class.level_one_choice["spells"] = get_all_spells_of_class_and_level(record[13], 1)
        if record[15] > 0:
            dnd_class.level_one_slots = record[15]
        if record[16] is not '':
            dnd_class.spell_casting_ability = record[16]
        return dnd_class
    return None

