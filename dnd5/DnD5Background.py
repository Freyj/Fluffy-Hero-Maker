

class DnD5Background:
    """
        Class that describes a background as defined in the DnD5 SRD rules allowing to recover information from it
    """
    def __init__(self, name: str):
        self.name = name
        self.skill_proficiencies = []
        self.tool_proficiencies = []
        self.bonus_languages = 0
        self.equipment = []
        self.feature = ""
        self.description = ""
        self.feature_description = ""
        self.feature_choice = ""
        self.feature_choice_table = []
        self.personality_traits = []
        self.ideals = []
        self.bonds = []
        self.flaws = []

    def to_string(self):
        """"
            Creates a describing string of the background, formatted with linebreaks and tabs
            :return a str of the background
        """
        resulting_string = 'Description of the background:\n'
        description_table = self.description.split('.')
        for i in description_table:
            resulting_string += '\t' + i.strip() + '\n'
        resulting_string = resulting_string[:-2]
        resulting_string += 'Feature: ' + self.feature + '\n'
        feature_desc_table = self.feature_description.split('.')
        for i in feature_desc_table:
            resulting_string += '\t' + i.strip() + '\n'
        resulting_string = resulting_string[:-2]
        if len(self.skill_proficiencies) > 0:
            resulting_string += 'Skill Proficiencies offered: '
            resulting_string += ", ".join(self.skill_proficiencies) + '\n'
        if len(self.tool_proficiencies) > 0:
            resulting_string += 'Tool Proficiencies offered: '
            resulting_string += ", ".join(self.tool_proficiencies) + '\n'
        if self.bonus_languages > 0:
            resulting_string += 'Number of bonus languages: ' + str(self.bonus_languages) + '\n'
        if len(self.equipment) > 0:
            resulting_string += "Equipment: " + ", ".join(self.equipment) + '\n'
        resulting_string = resulting_string[:-2]
        return resulting_string
