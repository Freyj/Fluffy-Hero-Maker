import json
import os

from characters.character import Character

from dnd5_character.dnd5_constants import ALIGNMENTS, ARMOR_PROFICIENCIES

from utils.utilities import is_valid_choice, generate_attributes, list_to_str, get_modifier


class Dnd5Character(Character):
    """
        Defines a player character in DnD according to 5e rules
    """
    def __init__(self, name, gen_type, stats=None):
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
        self.equipment = ""
        self.features = []
        self.hit_points = 0
        self.level = 1

    def set_attributes(self, attributes):
        """"Set the characters attributes, from a list of 6 integers"""
        if type(attributes) is list and len(attributes) is 6:
            for i in range(6):
                assert(20 > attributes[i] > 0)
            self.attributes = {
                "Strength": attributes[0],
                "Dexterity": attributes[1],
                "Constitution": attributes[2],
                "Intelligence": attributes[3],
                "Wisdom": attributes[4],
                "Charisma": attributes[5]
            }
        else:
            print("Error in the assignment of attributes:\nPossibly the number of attributes is wrong.")

    def calc_hp_first_lvl(self):
        """"Calculates hit points of character from first level, based on hit die of class and constitution
        modifier. Does not take into account other bonuses"""
        self.hit_points = self.dnd_class.hit_dice + get_modifier(self.attributes["Constitution"])

    def set_race(self, race):
        self.race = race
        self.add_racial_bonuses()

    def set_class(self, dnd_class):
        self.dnd_class = dnd_class
        self.add_class_bonuses()

    def set_background(self, dnd_background):
        self.background = dnd_background.name
        for i in dnd_background.skill_proficiencies:
            self.skill_proficiencies.add(i)
        for i in dnd_background.tool_proficiencies:
            self.tool_proficiencies.add(i)
        self.equipment += dnd_background.equipment

    def set_alignment(self, alignment):
        if is_valid_choice(ALIGNMENTS, alignment):
            self.alignment = ALIGNMENTS[alignment]

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

    def adjust_attributes_for_race(self):
        for i in self.race.abilities_plus_one:
            if i is not '':
                self.attributes[i] += 1
        for i in self.race.abilities_plus_two:
            if i is not '':
                self.attributes[i] += 2

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
        character_dict = {
            "name": self.name,
            "race": self.race.name,
            "class": self.dnd_class.name,
            "size": self.size,
            "attributes": self.attributes,
            "languages": list_to_str(self.languages),
            "skill_proficiencies": list_to_str(self.skill_proficiencies),
            "tool_proficiencies": list_to_str(self.tool_proficiencies),
            "armor_proficiencies": list_to_str(self.armor_proficiencies),
            "weapon_proficiencies": list_to_str(self.weapon_proficiencies),
            "age": self.age,
            "vision": list_to_str(self.vision),
            "proficiency_bonus": self.proficiency_bonus,
            "hit_points": self.hit_points
        }
        return json.dumps(character_dict)

    def create_character_from_json(self):
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
