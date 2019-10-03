from utils.utilities import dict_to_str_for_speed


class DnD5Race:
    def __init__(self, name):
        self.name = name
        self.hit_dice = 4
        self.abilities_plus_two = []
        self.abilities_plus_one = []
        self.abilities_choice_plus_one = {
            "number": 0,
            "abilities": []
        }
        self.abilities_choice_plus_two = {
            "number": 0,
            "abilities": []
        }
        self.quick_description = ""
        # using the standard size of d as M so that you only have to add it when it's not a medium sized creature ?
        self.size = 'Medium'
        self.vision = ["Normal"]
        self.languages = set([])
        self.bonus_languages = 0
        self.speed = {
            "walking": 30
        }
        self.skill_proficiencies = set([])
        self.skill_proficiency_choices = {
            "number": 0,
            "skill_proficiencies": []
        }
        self.tool_proficiencies = set([])
        self.armor_proficiencies = set([])
        self.tool_proficiency_choices = {
            "number": 0,
            "tool_proficiency": []
        }
        self.age_bracket = []
        self.racial_traits = []
        self.cantrips_choice = {
            "number": 0,
            "cantrips": []
        }
        self.cantrips_to_add = []
        self.spells_to_add = []
        self.weapon_proficiencies_to_add = []
        self.racial_traits_to_choose = {
            "number": 0,
            "traits": []
            # Commented to show structure it is supposed to have
            # "number": 0,
            # "traits": [
            #     {
            #         "name": "name",
            #         "description": "description",
            #         "links": "links",
            #         "list": []
            #     }
            # ]
        }

    def add_language(self, language):
        self.languages.add(language)

    def add_skill_proficiency(self, skill_proficiency):
        self.skill_proficiencies.add(skill_proficiency)

    def add_tool_proficiency(self, tool_proficiency):
        self.tool_proficiencies.add(tool_proficiency)

    def racial_traits_to_string(self):
        result_string = ""
        for i in self.racial_traits:
            result_string += "\tName: " + i["name"] +"\n"
            result_string += "\t\t" + i["description"] + "\n"
        result_string = result_string[:-2]
        return result_string

    def get_racial_traits(self):
        """returns a tuple of racial traits choice number and racial traits choices description"""
        racial_traits_choices_nb = self.racial_traits_to_choose["number"]
        racial_traits_choices_list = self.racial_traits_to_choose["traits"]
        return racial_traits_choices_nb, racial_traits_choices_list

    def get_racial_tools(self):
        """returns a tuple of racial tools choice number and racial tools choices description"""
        tool_choices_nb = self.tool_proficiency_choices["number"]
        tool_choices = self.tool_proficiency_choices["tool_proficiency"]
        return tool_choices_nb, tool_choices

    def get_racial_cantrips(self):
        """returns a tuple of racial cantrips choice number and racial cantrips choices description"""
        cantrip_choice_nb = self.cantrips_choice["number"]
        cantrip_choice_list = self.cantrips_choice["cantrips"]
        return cantrip_choice_nb, cantrip_choice_list

    def get_racial_skills_choices(self):
        """returns a tuple of racial skill proficiencies choice number and racial proficiencies choices description"""
        skill_choice_number = self.skill_proficiency_choices["number"]
        skill_choice_options = self.skill_proficiency_choices["skill_proficiencies"]
        return skill_choice_number, skill_choice_options

    def to_cli_string(self):
        resulting_string = "Race: " + self.name + "\n"
        resulting_string += "Size: " + self.size + "\n"
        resulting_string += "Abilities augmented by 1: " + ", ".join(self.abilities_plus_one) + "\n"
        resulting_string += "Abilities augmented by 2: " + ", ".join(self.abilities_plus_two) + "\n"
        if len(self.languages) > 0:
            resulting_string += "Languages added: " + ", ".join(self.languages) + "\n"
        if self.bonus_languages > 0:
            resulting_string += "Bonus language choices: " + str(self.bonus_languages) + "\n"
        if len(self.skill_proficiencies) > 0:
            resulting_string += "Skill proficiencies added: " + ", ".join(self.skill_proficiencies) + "\n"
        resulting_string += "Speed:\n" + dict_to_str_for_speed(self.speed)
        resulting_string += "Vision: " + ", ".join(self.vision) + "\n"
        resulting_string += "Age from " + self.age_bracket[0] + " to " + self.age_bracket[1] + "\n"
        if len(self.racial_traits) > 0:
            resulting_string += "Racial traits:\n" + self.racial_traits_to_string()
        if len(self.spells_to_add) > 0:
            resulting_string += "Bonus spells: " + ", ".join(self.spells_to_add)
        if len(self.weapon_proficiencies_to_add) > 0:
            resulting_string += "Weapon Proficiencies: " + ", ".join(self.weapon_proficiencies_to_add)
        if self.racial_traits_to_choose["number"] > 0:
            resulting_string += "Racial Traits to Choose from:\n"
            for i in range(len(self.racial_traits_to_choose["traits"])):
                resulting_string += "\tName: " + self.racial_traits_to_choose["traits"][i]["name"] + "\n"
                resulting_string += "\tDescription: " + self.racial_traits_to_choose["traits"][i]["description"] + "\n"
                resulting_string += "\tLinked to: " + self.racial_traits_to_choose["traits"][i]["links"] + "\n"
                resulting_string += "\tChoices: " + ", ".join(self.racial_traits_to_choose["traits"][i]["list"]) + "\n"
        return resulting_string
