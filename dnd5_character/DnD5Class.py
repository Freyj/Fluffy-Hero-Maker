

class DnD5Class:
    def __init__(self, name):
        self.name = name
        # the hit dice will be 6 for 1d6, 8 for 1d8, 10 for 1d10, 12 for 1d12 ...
        self.hit_dice = 0
        self.skill_proficiency_choices = {
            "number": 0,
            "skill_list": []
        }
        self.tool_proficiency_choices = {
            "number": 0,
            "tool_proficiencies": []
        }
        self.armor_proficiencies_to_add = []
        self.weapon_proficiencies_to_add = []
        self.tool_proficiencies_to_add = []
        self.class_features = []
        self.class_feature_choices = []
        self.level = 1
        self.spellcaster_class = ""
        self.spell_casting_ability = ""
        self.cantrips_choice = {
            "number": 0,
            "cantrips": []
        }
        self.level_one_choice = {
            "number": 0,
            "spells": []
        }
        self.is_spellcaster = False
        self.is_divine_spellcaster = False
        self.level_one_slots = 0
        self.level_two_slots = 0
        self.level_three_slots = 0
        self.level_four_slots = 0
        self.level_five_slots = 0
        self.level_six_slots = 0
        self.class_features = []
        self.saving_throws = []
        self.added_equipment = []
        self.equipment_choice = ""

    def choose_feature(self, feature_name, choice):
        feature = self.find_choice_in_features(feature_name, choice)
        if feature != {}:
            self.class_features.append(feature)

    def find_choice_in_features(self, feature_name, choice):
        result = {}
        for feature in self.class_feature_choices:
            if feature["name"] is feature_name:
                for item in feature["choice_table"]:
                    if choice == item["name"]:
                        description = item["description"]
                        result = {
                            "name": feature_name + ': ' + choice,
                            "description": description
                        }
        return result

    def to_cli_string(self):
        resulting_string = "Class: " + self.name + "\n"
        resulting_string += "Hit Dice: " + str(self.hit_dice) + "\n"
        class_features_string = self.class_features_to_string()
        resulting_string += "Class Features:\n" + class_features_string
        resulting_string += "\nWeapon Proficiencies: " + ", ".join(self.weapon_proficiencies_to_add)
        resulting_string += "\nArmor Proficiencies: " + ", ".join(self.armor_proficiencies_to_add)
        if len(self.tool_proficiencies_to_add) > 0:
            resulting_string += "\nTool Proficiencies: " + ", ".join(self.tool_proficiencies_to_add)
        resulting_string += "\nSaving Throws: " + ", ".join(self.saving_throws)
        if len(self.class_feature_choices) > 0:
            class_feature_choices_string = self.class_feature_choices_to_string()
            resulting_string += "\nClass Feature Choices:\n" + class_feature_choices_string
        resulting_string += '\nEquipment offered: '
        if len(self.added_equipment) > 0:
            resulting_string += '\n\t'
            resulting_string += ", ".join(self.added_equipment)
        if self.equipment_choice != '':
            resulting_string += '\n' + self.equipment_to_string()
        if self.spellcaster_class:
            resulting_string += '\nSpellcasting:\n'
            resulting_string += self.cantrips_to_string() + '\n'
            resulting_string += self.spells_to_string()
        return resulting_string

    def class_features_to_string(self):
        resulting_string = ''
        for feature in self.class_features:
            resulting_string += '\t' + feature["name"] + '\n'
            description_string = ''
            split_desc = feature["description"].split('.')
            for desc in split_desc:
                if desc is not '':
                    desc = desc.strip() + '.'
                    description_string += "\t\t" + desc + "\n"
            resulting_string += description_string
        resulting_string = resulting_string[:-1]
        return resulting_string

    def class_feature_choices_to_string(self):
        resulting_string = ""
        for choice in self.class_feature_choices:
            resulting_string += '\t' + choice["name"] + ':\n' + choice["description"] + '\n'
            for item in choice["choice_table"]:
                resulting_string += '\t\t' + item["name"] + '\n'
                if item["description"] is not '':
                    resulting_string += '\t\t\t' + item["description"] + '\n'
        resulting_string = resulting_string[:-2]
        return resulting_string

    def equipment_to_string(self):
        resulting_string = ''
        choices = self.equipment_choice.split('#')
        for choice in choices:
            options = choice.split('/')
            resulting_string += '\t'
            for option in options:
                resulting_string += option + ' or '
            resulting_string = resulting_string[:-4]
        return resulting_string

    def cantrips_to_string(self):
        resulting_string = "You can choose " + str(self.cantrips_choice["number"]) + " cantrips:\n"
        resulting_string += ", ".join(self.cantrips_choice["cantrips"])
        return resulting_string

    def spells_to_string(self):
        resulting_string = ""
        if self.level_one_choice["number"] > 0:
            resulting_string += "You can choose " + str(self.level_one_choice["number"]) + " spells:\n"
            resulting_string += ", ".join(self.level_one_choice["spells"])
        resulting_string += "You will have " + str(self.level_one_slots) + " slots for level one spells."
        return resulting_string
