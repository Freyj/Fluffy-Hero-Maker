class DnD5Spell:
    """
        Class representing a spell according to DnD 5 rules (srd)
    """
    def __init__(self, name: str):
        self.name = name
        self.school = ""
        self.casting_time = ""
        self.range = ""
        self.components = ""
        self.duration = ""
        self.level = 0
        self.description = ""
        self.saving_throw = ""
        self.concentration = False
        self.upgrade = ""
        self.ritual = False
        self.classes = []

    def cli_description_string(self):
        """
            Returns a string with the description formatted with tabs and linebreaks
            :return: str
        """
        resulting_string = ""
        string_list = self.description.split('.')[:-1]
        for i in string_list:
            i = i.strip()
            resulting_string += "\t" + i + ".\n"
        return resulting_string[:-2]
