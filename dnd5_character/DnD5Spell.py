class DnD5Spell:
    def __init__(self, name):
        self.name = name
        self.school = ""
        self.casting_time = ""
        self.range = ""
        self.components = ""
        self.duration = ""
        self.level = 0
        self.description = ""
        self.saving_throw = ""
        self.concentration = ""
        self.upgrade = ""
        self.ritual = ""
        self.classes = []

    def cli_description_string(self):
        resulting_string = ""
        string_list = self.description.split('.')[:-1]
        for i in string_list:
            i = i.strip()
            resulting_string += "\t" + i + ".\n"
        return resulting_string[:-2]
