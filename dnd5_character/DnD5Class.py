from utils.utilities import list_to_str


class DnD5Class:
    def __init__(self, name):
        self.name = name
        # the hit dice will be 6 for 1d6, 8 for 1d8, 10 for 1d10, 12 for 1d12 ...
        self.hit_dice = 0
        self.skill_proficiency_choices = {
            "number": 0,
            "skill_proficiencies": []
        }
        self.tool_proficiency_choices = {
            "number": 0,
            "tool_proficiencies": []
        }
        self.armor_proficiencies_to_add = []
        self.weapon_proficiencies_to_add = []
        self.class_features = []
        self.feature_choices = []
        self.level = 1
        self.cantrips_choice = {
            "number": 0,
            "cantrips": []
        }
        self.level_one_choice = {
            "number": 0,
            "spells": []
        }
        self.is_spellcaster = False
        self.level_one_slots = 0
        self.level_two_slots = 0
        self.level_three_slots = 0
        self.level_four_slots = 0
        self.level_five_slots = 0
        self.level_six_slots = 0
        self.class_features = []

    def choose_feature(self, feature_name, feature_choice):
        pass

    def to_cli_string(self):
        resulting_string = "Class: " + self.name + "\n"
        resulting_string += "Hit Dice: " + str(self.hit_dice) + "\n"
        # class_features = self.display_class_features_with_description()
        # resulting_string += class_features
        resulting_string += list_to_str(self.class_features)
        resulting_string += "\nWeapon Proficiencies: " + list_to_str(self.weapon_proficiencies_to_add)
        resulting_string += "\nArmor Proficiencies: " + list_to_str(self.armor_proficiencies_to_add)
        return resulting_string
