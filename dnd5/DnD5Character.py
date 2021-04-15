import json
import os
import random

from characters.character import Character
from databases.dnd5.dnd5_backgrounds_db import get_all_background_names, get_background_by_name
from databases.dnd5.dnd5_classes_db import get_all_classes_names, get_class_by_name
from databases.dnd5.dnd5_languages_db import get_all_languages, get_all_unrestricted_languages
from databases.dnd5.dnd5_races_db import get_all_races_names, look_for_race_by_name
from dnd5.DnD5Background import DnD5Background
from dnd5.dnd5_constants import ALIGNMENTS, ARMOR_PROFICIENCIES
from utils.utilities import is_valid_choice, generate_attributes, get_modifier


class DnD5Character(Character):
    """
        Defines a character in DnD according to 5e srd rules
    """
    def __init__(self, name: str, gen_type: int, stats=None):
        """
        Initializes the character
            @:param name: a string to be the name of the character
            @:param gen_type: an int to describe the type of generation wanted
                1: 4d6 drop lowest
                2: 3d6
                3: 3d6 re-roll lower than 7 (8?)
                4: pick all 6
                5: re-roll if not 3 < bonus < 7 (cf utilities.py generate_abilities)
            @:param stats: an array of stats, only there when gen_type is 4
            Computes derived attributes such as Base Saving Throws
        """
        super().__init__()

        self.name = name
        self.attributes = generate_attributes(gen_type, stats)
        self.race = None
        self.dnd_class = None
        self.background = None
        self.size = 'Medium'
        self.speed = {
            "walking": 30
        }
        self.saving_throws = {
            "Strength": get_modifier(self.attributes["Strength"]),
            "Dexterity": get_modifier(self.attributes["Dexterity"]),
            "Constitution": get_modifier(self.attributes["Constitution"]),
            "Intelligence": get_modifier(self.attributes["Intelligence"]),
            "Wisdom": get_modifier(self.attributes["Wisdom"]),
            "Charisma": get_modifier(self.attributes["Charisma"]),
        }
        self.proficient_saving_throws = []
        self.languages = {"Common"}
        self.skill_proficiencies = set([])
        self.tool_proficiencies = set([])
        self.armor_proficiencies = set([])
        self.weapon_proficiencies = set([])
        self.age = 0
        self.vision = []
        # starting proficiency bonus is always 2
        self.proficiency_bonus = 2
        self.alignment = ""
        self.cantrips = set([])
        self.spells = set([])
        self.prepared_spell_number = 0
        self.level_one_slots = 0
        self.level_two_slots = 0
        self.level_three_slots = 0
        self.level_four_slots = 0
        self.level_five_slots = 0
        self.level_six_slots = 0
        self.personality_traits = []
        self.ideals = []
        self.bonds = []
        self.flaws = []
        self.equipment = []
        self.features = []
        self.hit_points = 0
        self.level = 1

    def set_attributes(self, attributes):
        """"
            Set the characters attributes, from a list of 6 integers
            @:param attributes: a list of integer between 1 and 20
        """

        if isinstance(attributes, list) and len(attributes) == 6:
            self.attributes = {
                "Strength": attributes[0],
                "Dexterity": attributes[1],
                "Constitution": attributes[2],
                "Intelligence": attributes[3],
                "Wisdom": attributes[4],
                "Charisma": attributes[5]
            }
        else:
            # TODO: throw exception instead of printing stuff
            print("Error in the assignment of attributes:\nPossibly the number of attributes is wrong.")

    def calc_hp_first_lvl(self):
        """"
            Updates hit points of character for first level, based on hit die of class and constitution
            modifier. Does not take into account other bonuses.
        """
        self.hit_points = self.dnd_class.hit_dice + get_modifier(self.attributes["Constitution"])

    def set_race(self, race):
        """
            Sets up the race of the character and applies the racial bonuses
            :param race: a DnD5Race object
            :return: nothing
        """
        self.race = race
        self.add_racial_bonuses()

    def set_class(self, dnd_class):
        """
            Sets up the class of the character and applies the class bonuses
            :param dnd_class: a DnD5Class object
            :return: nothing
        """
        self.dnd_class = dnd_class
        self.add_class_bonuses()

    def set_background(self, dnd_background: DnD5Background):
        """
            Sets up the background of the character and applies the background bonuses, adding skill and tool
            proficiencies and adding equipment
            :param dnd_background: a DnD5Background object
            :return: nothing
        """
        self.background = dnd_background.name
        for i in dnd_background.skill_proficiencies:
            self.skill_proficiencies.add(i)
        for i in dnd_background.tool_proficiencies:
            self.tool_proficiencies.add(i)
        self.equipment.extend(dnd_background.equipment)

    def set_alignment(self, alignment: str):
        """
            Sets the alignment of the character
            :param alignment: a string that has to be in the array dnd5_character.dnd5_constants.ALIGNMENTS
            :return: nothing
        """
        if is_valid_choice(ALIGNMENTS, alignment):
            self.alignment = ALIGNMENTS[alignment]
        # TODO: if the choice is not valid, something should be done instead of silently doing nothing (at least
        # reporting)

    def set_bonus_skill_proficiencies(self, skill_proficiencies):
        for i in skill_proficiencies:
            self.skill_proficiencies.add(i)

    def set_bonus_tool_proficiencies(self, tool_proficiencies):
        for i in tool_proficiencies:
            self.tool_proficiencies.add(i)

    def set_bonus_languages(self, languages):
        for i in languages:
            self.languages.add(i)

    def set_age(self, age):
        self.age = age

    def add_racial_bonuses(self):
        self.adjust_attributes_for_race()
        self.adjust_languages_from_race()
        self.adjust_spells_from_race()
        self.adjust_skill_proficiencies_from_race()
        self.adjust_armor_proficiencies_from_race()
        self.adjust_weapon_proficiencies_from_race()
        self.vision = self.race.vision

    def add_class_bonuses(self):
        self.adjust_armor_from_class()
        self.adjust_weapon_from_class()
        self.adjust_tools_from_class()
        self.adjust_saving_throws_from_class()
        if len(self.dnd_class.added_equipment) > 0:
            self.equipment.extend(self.dnd_class.added_equipment)

    def update_saving_throws(self):
        self.saving_throws = {
            "Strength": get_modifier(self.attributes["Strength"]),
            "Dexterity": get_modifier(self.attributes["Dexterity"]),
            "Constitution": get_modifier(self.attributes["Constitution"]),
            "Intelligence": get_modifier(self.attributes["Intelligence"]),
            "Wisdom": get_modifier(self.attributes["Wisdom"]),
            "Charisma": get_modifier(self.attributes["Charisma"]),
        }

    def adjust_attributes_for_race(self):
        for i in self.race.abilities_plus_one:
            if i != '':
                self.attributes[i] += 1
        for i in self.race.abilities_plus_two:
            if i != '':
                self.attributes[i] += 2
        self.update_saving_throws()

    def add_equipment(self, item):
        if item != '':
            self.equipment.append(item)

    def adjust_armor_from_class(self):
        for proficiency in self.dnd_class.armor_proficiencies_to_add:
            if is_valid_choice(ARMOR_PROFICIENCIES, proficiency):
                self.armor_proficiencies.add(proficiency)

    def adjust_tools_from_class(self):
        for proficiency in self.dnd_class.tool_proficiencies_to_add:
            self.tool_proficiencies.add(proficiency)

    def adjust_saving_throws_from_class(self):
        self.proficient_saving_throws = self.dnd_class.saving_throws
        for saving_throw in self.dnd_class.saving_throws:
            self.saving_throws[saving_throw] += self.proficiency_bonus

    def add_cantrip(self, cantrip):
        self.cantrips.add(cantrip)

    def add_spell(self, spell):
        self.spells.add(spell)

    def add_spell_slots(self):
        if self.dnd_class.is_spellcaster:
            self.level_one_slots += self.dnd_class.level_one_slots
            self.level_two_slots += self.dnd_class.level_two_slots
            self.level_three_slots += self.dnd_class.level_three_slots
            self.level_four_slots += self.dnd_class.level_four_slots
            self.level_five_slots += self.dnd_class.level_five_slots
            self.level_six_slots += self.dnd_class.level_six_slots

    def adjust_languages_from_race(self):
        for i in self.race.languages:
            self.languages.add(i)

    def adjust_skill_proficiencies_from_race(self):
        for i in self.race.skill_proficiencies:
            self.skill_proficiencies.add(i)

    def adjust_armor_proficiencies_from_race(self):
        for i in self.race.armor_proficiencies:
            self.armor_proficiencies.add(i)

    def adjust_spells_from_race(self):
        for i in self.race.cantrips_to_add:
            self.cantrips.add(i)
        for i in self.race.spells_to_add:
            self.spells.add(i)

    def create_json_from_character(self):
        # TODO: have more info, find better way to do it (json.dumps?)
        character_dict = {
            "name": self.name,
            "race": self.race.name,
            "class": self.dnd_class.name,
            "size": self.size,
            "attributes": self.attributes,
            "languages": ", ".join(self.languages),
            "skill_proficiencies": ", ".join(self.skill_proficiencies),
            "tool_proficiencies": ", ".join(self.tool_proficiencies),
            "armor_proficiencies": ", ".join(self.armor_proficiencies),
            "weapon_proficiencies": ", ".join(self.weapon_proficiencies),
            "age": self.age,
            "vision": ", ".join(self.vision),
            "proficiency_bonus": self.proficiency_bonus,
            "hit_points": self.hit_points
        }
        return json.dumps(character_dict, indent=2, separators=(',', ': '))

    def create_character_from_json(self):
        # TODO: function to load a character from json
        pass

    def export_json(self):
        script_dir = os.path.dirname(__file__)
        file_name = script_dir + '/saves/' + self.name + '.json'
        json_export = self.create_json_from_character()
        with open(file_name, 'w') as f:
            f.write(json_export)
        f.close()

    def adjust_weapon_proficiencies_from_race(self):
        for proficiency in self.race.weapon_proficiencies_to_add:
            self.weapon_proficiencies.add(proficiency)

    def adjust_weapon_from_class(self):
        for proficiency in self.dnd_class.weapon_proficiencies_to_add:
            self.weapon_proficiencies.add(proficiency)

    def saving_throws_to_str(self):
        saving_throw_str = "\n\tStrength: " + str(self.saving_throws["Strength"])
        saving_throw_str += "\n\tDexterity: " + str(self.saving_throws["Dexterity"])
        saving_throw_str += "\n\tConstitution: " + str(self.saving_throws["Constitution"])
        saving_throw_str += "\n\tIntelligence: " + str(self.saving_throws["Intelligence"])
        saving_throw_str += "\n\tWisdom: " + str(self.saving_throws["Wisdom"])
        saving_throw_str += "\n\tCharisma: " + str(self.saving_throws["Charisma"])
        return saving_throw_str

    def attributes_to_str(self):
        attributes_str = "\n\tStrength: " + str(self.attributes["Strength"])
        attributes_str += "\n\tDexterity: " + str(self.attributes["Dexterity"])
        attributes_str += "\n\tConstitution: " + str(self.attributes["Constitution"])
        attributes_str += "\n\tIntelligence: " + str(self.attributes["Intelligence"])
        attributes_str += "\n\tWisdom: " + str(self.attributes["Wisdom"])
        attributes_str += "\n\tCharisma: " + str(self.attributes["Charisma"])
        return attributes_str

    def equipment_to_string(self):
        """Displays a string representing the equipment of the character"""
        equipment_str = ""
        item_counter = 0
        for item in self.equipment:
            equipment_str += item + ", "
            item_counter += 1
            if item_counter % 5  == 0:
                equipment_str += "\n"
        equipment_str.strip()
        equipment_str = equipment_str[:-2]
        return equipment_str


def generate_random_dnd_character(name: str):
    """
        Generates a random DnD character
        :return: a DnD5Character randomly generated
    """
    if name is None:
        name = "I ncognito"
    dnd_char = DnD5Character(name, gen_type=1)
    # lists
    race_name_list = get_all_races_names()
    background_name_list = get_all_background_names()
    # language_list = get_all_languages()
    classes_list = get_all_classes_names()
    # unrestricted_language_list = get_all_unrestricted_languages()

    # randomly pick a race
    race_result = random.randint(0, len(race_name_list) - 1)
    race = look_for_race_by_name(race_name_list[race_result])
    dnd_char.set_race(race)

    # randomly choose an age
    age_result = random.randint(int(race.age_bracket[0]), int(race.age_bracket[1]))
    dnd_char.set_age(age_result)

    # randomly choose a background
    background_result = random.randint(0, len(background_name_list) - 1)
    background = get_background_by_name(background_name_list[background_result])
    dnd_char.set_background(background)

    class_result = random.randint(0, len(classes_list) - 1)
    class_choice = get_class_by_name(classes_list[class_result])
    dnd_char.set_class(class_choice)

    return dnd_char
