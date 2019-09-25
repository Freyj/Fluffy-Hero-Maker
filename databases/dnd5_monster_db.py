import json
import os
import sqlite3

from dnd5_monsters.dnd5_monster import DnD5Monster
from utils.dice_roller import roll_die
from utils.utilities import list_to_str

MONSTER_DATA_DIR = 'databases/data/monsters/'

CREATE_MONSTER_TABLE_REQUEST = '''CREATE TABLE IF NOT EXISTS dnd5_monsters 
                            (id integer primary key, name text not null, size text, alignment text, monster_type text,
                             strength numeric, dexterity numeric, constitution numeric, intelligence numeric, 
                             wisdom numeric, charisma numeric, walking_speed numeric, climbing_speed numeric,
                             burrowing_speed numeric, flying_speed numeric, swimming_speed numeric, 
                             save_throw_strength, save_throw_dexterity, save_throw_constitution, 
                             save_throw_intelligence, save_throw_wisdom, save_throw_charisma, armor_class, hit_points,
                             hit_dice, passive_perception, xp, challenge, damage_immunities text, damage_resistance,
                             condition_immunities, senses, languages_spoken, languages_understood, actions, attacks,
                             traits, cantrips, spells_lvl1, spell_slots_lvl1, spells_lvl2, spell_slots_lvl2, 
                             spells_lvl3, spell_slots_lvl3, spells_lvl4, spell_slots_lvl4, spells_lvl5, 
                             spell_slots_lvl5, spells_lvl6, spell_slots_lvl6, spells_lvl7, spell_slots_lvl7,
                             spells_lvl8, spell_slots_lvl8, spells_lvl9, spell_slots_lvl9, description)'''


DROP_MONSTER_TABLE_REQUEST = '''DROP TABLE IF EXISTS dnd5_monsters'''


def get_number_of_monsters_in_db():
    """Returns an integer of the number of monsters in the database"""
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()

    select_request = '''SELECT count() from dnd5_monsters'''
    cursor.execute(select_request)
    number_of_rows = cursor.fetchone()[0]
    connection.close()
    return number_of_rows


def from_attacks_dictionary_to_string(attacks):
    attacks_string = ""
    for attack in attacks:
        temp_string = '[' + attack["name"] + ';' + attack["type"] + ';' + str(attack["hit_bonus"])
        temp_string += ';' + attack["target"] + ';' + attack["specials"] + ';' + attack["damage"]
        if attack["on_hit"] is not '':
            temp_string += ';' + attack["on_hit"]
        attacks_string += temp_string + ']:'
    attacks_string = attacks_string[:-1]
    return attacks_string


def get_all_monsters_from_json():
    monsters = []
    for file in os.listdir(MONSTER_DATA_DIR):
        file_path = MONSTER_DATA_DIR + file
        if file_path.endswith(".json"):
            with open(file_path) as fd:
                json_data = json.load(fd)
                for monster in json_data:
                    attacks = monster["attacks"]
                    attacks_string = from_attacks_dictionary_to_string(attacks)
                    element = (monster["name"],
                               monster["size"],
                               monster["alignment"],
                               monster["monster_type"],
                               monster["strength"],  # 5
                               monster["dexterity"],
                               monster["constitution"],
                               monster["intelligence"],
                               monster["wisdom"],
                               monster["charisma"],  # 10
                               monster["walking_speed"],
                               monster["burrowing_speed"],
                               monster["climbing_speed"],
                               monster["flying_speed"],
                               monster["swimming_speed"],  # 15
                               monster["save_throw_strength"],
                               monster["save_throw_dexterity"],
                               monster["save_throw_constitution"],
                               monster["save_throw_intelligence"],
                               monster["save_throw_wisdom"],  # 20
                               monster["save_throw_charisma"],
                               monster["armor_class"],
                               monster["hit_points"],
                               monster["hit_dice"],
                               monster["passive_perception"],  # 25
                               monster["xp"],
                               monster["challenge"],
                               list_to_str(monster["damage_immunities"]),
                               list_to_str(monster["damage_resistance"]),
                               list_to_str(monster["condition_immunities"]),  # 30
                               list_to_str(monster["senses"]),
                               list_to_str(monster["languages_spoken"]),
                               list_to_str(monster["languages_understood"]),
                               list_to_str(monster["actions"]),
                               attacks_string,  # 35
                               list_to_str(monster["traits"]),
                               list_to_str(monster["cantrips"]),
                               list_to_str(monster["spells_lvl1"]),
                               monster["spell_slots_lvl1"],
                               list_to_str(monster["spells_lvl2"]),
                               monster["spell_slots_lvl2"],  # 40
                               list_to_str(monster["spells_lvl3"]),
                               monster["spell_slots_lvl3"],
                               list_to_str(monster["spells_lvl4"]),
                               monster["spell_slots_lvl4"],
                               list_to_str(monster["spells_lvl5"]),  # 45
                               monster["spell_slots_lvl5"],
                               list_to_str(monster["spells_lvl6"]),
                               monster["spell_slots_lvl6"],
                               list_to_str(monster["spells_lvl7"]),
                               monster["spell_slots_lvl7"],  # 50
                               list_to_str(monster["spells_lvl8"]),
                               monster["spell_slots_lvl8"],
                               list_to_str(monster["spells_lvl9"]),
                               monster["spell_slots_lvl9"],
                               monster["description"]
                               )
                    monsters.append(element)
    return monsters


def insert_dnd5_monster_data():
    if get_number_of_monsters_in_db() == 0:
        monsters = get_all_monsters_from_json()
        if len(monsters) > 0:
            connection = sqlite3.connect('dnd5_db.db')
            connection.executemany("INSERT INTO dnd5_monsters(name, size, alignment, monster_type, strength, "
                                   "dexterity, constitution, intelligence, wisdom, charisma, walking_speed, "
                                   "climbing_speed, burrowing_speed, flying_speed, swimming_speed, "
                                   "save_throw_strength, save_throw_dexterity, save_throw_constitution, "
                                   "save_throw_intelligence, save_throw_wisdom, save_throw_charisma, armor_class, "
                                   "hit_points, hit_dice, passive_perception, xp, challenge, damage_immunities, "
                                   "damage_resistance, condition_immunities, senses, languages_spoken, "
                                   "languages_understood, actions, attacks, traits, cantrips, spells_lvl1, "
                                   "spell_slots_lvl1, spells_lvl2, spell_slots_lvl2, spells_lvl3, spell_slots_lvl3, "
                                   "spells_lvl4, spell_slots_lvl4, spells_lvl5, spell_slots_lvl5, spells_lvl6, "
                                   "spell_slots_lvl6, spells_lvl7, spell_slots_lvl7, spells_lvl8, spell_slots_lvl8, "
                                   "spells_lvl9, spell_slots_lvl9, description) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?"
                                   ",?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                   monsters)
            connection.commit()
            connection.close()


def get_monster_by_name(monster_name):
    monster = DnD5Monster("test")
    if monster_name != "":
        connection = sqlite3.connect('dnd5_db.db')
        cursor = connection.cursor()
        select_request = '''SELECT * from dnd5_monsters WHERE name = (?) '''
        cursor.execute(select_request, (monster_name,))
        record = cursor.fetchone()
        monster = change_record_into_monster(record)
        connection.close()
        return monster
    return None


def get_all_monsters_names_from_db():
    names = []
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT name from dnd5_monsters'''
    cursor.execute(select_request)
    records = cursor.fetchall()
    for i in records:
        names.append(i[0])
    return names


def get_all_monsters_names_by_type(monster_type):
    names = []
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT name from dnd5_monsters where monster_type = (?)'''
    cursor.execute(select_request, (monster_type,))
    records = cursor.fetchall()
    for i in records:
        names.append(i[0])
    return names


def get_random_monster():
    number = get_number_of_monsters_in_db()
    roll = roll_die(number)
    monster = get_monster_by_id(roll)
    return monster


def get_monster_by_id(monster_id):
    if monster_id > -1:
        connection = sqlite3.connect('dnd5_db.db')
        cursor = connection.cursor()
        select_request = '''SELECT * from dnd5_monsters WHERE id = (?) '''
        cursor.execute(select_request, (monster_id,))
        record = cursor.fetchone()
        monster = change_record_into_monster(record)
        connection.close()
        return monster
    return None


def change_record_into_monster(record):
    """take a record tuple and change it into a DnD5Monster"""
    monster = DnD5Monster("temp")
    if record is not None:
        monster.name = record[1]
        monster.size = record[2]
        monster.alignment = record[3]
        monster.monster_type = record[4]
        monster.attributes["Strength"] = record[5]
        monster.attributes["Dexterity"] = record[6]
        monster.attributes["Constitution"] = record[7]
        monster.attributes["Intelligence"] = record[8]
        monster.attributes["Wisdom"] = record[9]
        monster.attributes["Charisma"] = record[10]
        monster.speed = {
            "walking_speed": record[11],
            "climbing_speed": record[12],
            "burrowing_speed": record[13],
            "flying_speed": record[14],
            "swimming_speed": record[15]
        }
        monster.saving_throws = {
            "Strength": record[16],
            "Dexterity": record[17],
            "Constitution": record[18],
            "Intelligence": record[19],
            "Wisdom": record[20],
            "Charisma": record[21]
        }
        monster.armor_class = record[22]
        monster.hit_points = record[23]
        monster.hit_dice = record[24]
        monster.passive_perception = record[25]
        monster.xp = record[26]
        monster.challenge = record[27]
        monster.damage_immunities = record[28].split(', ')
        monster.damage_resistances = record[29].split(', ')
        monster.condition_immunities = record[30].split(', ')
        monster.senses = record[31].split(', ')
        monster.languages_spoken = record[32].split(', ')
        monster.languages_understood = record[33].split(', ')
        monster.actions = record[34]
        monster.attacks = record[35]
        monster.traits = record[36]
        monster.cantrips = record[37]
        monster.spells_lvl_1["spells"] = record[38].split(', ')
        monster.spells_lvl_1["slot_number"] = record[39]
        monster.spells_lvl_2["spells"] = record[40].split(', ')
        monster.spells_lvl_2["slot_number"] = record[41]
        monster.spells_lvl_3["spells"] = record[42].split(', ')
        monster.spells_lvl_3["slot_number"] = record[43]
        monster.spells_lvl_4["spells"] = record[44].split(', ')
        monster.spells_lvl_4["slot_number"] = record[45]
        monster.spells_lvl_5["spells"] = record[46].split(', ')
        monster.spells_lvl_5["slot_number"] = record[47]
        monster.spells_lvl_6["spells"] = record[48].split(', ')
        monster.spells_lvl_6["slot_number"] = record[49]
        monster.spells_lvl_7["spells"] = record[50].split(', ')
        monster.spells_lvl_7["slot_number"] = record[51]
        monster.spells_lvl_8["spells"] = record[52].split(', ')
        monster.spells_lvl_8["slot_number"] = record[53]
        monster.spells_lvl_9["spells"] = record[54].split(', ')
        monster.spells_lvl_9["slot_number"] = record[55]
        monster.description = record[56]
        return monster
    return None
