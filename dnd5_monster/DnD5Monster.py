

class DnD5Monster:
    """
        Class describing monsters according to DnD 5 rules (srd)
    """
    def __init__(self, name: str):
        self.name = name
        self.size = "M"
        self.alignment = "Neutral"
        self.monster_type = ""
        self.description = ""
        self.attributes = {
            "Strength": 0,
            "Dexterity": 0,
            "Constitution": 0,
            "Intelligence": 0,
            "Wisdom": 0,
            "Charisma": 0
        }
        self.speed = {
            "walking": 30
        }
        self.saving_throws = {
            "Strength": 0,
            "Dexterity": 0,
            "Constitution": 0,
            "Intelligence": 0,
            "Wisdom": 0,
            "Charisma": 0
        }
        self.armor_class = 10
        self.hit_points = 10
        self.hit_dice = "1d10"
        self.passive_perception = 10
        self.xp = 100
        self.damage_immunities = []
        self.damage_resistances = []
        self.condition_immunities = []
        self.senses = []
        self.challenge = 1
        self.languages_spoken = []
        self.languages_understood = []
        self.actions = []
        self.legendary_actions = []
        self.attacks = []
        self.cantrips = []
        self.traits = [
            {
                "name": "name",
                "effect": "effect"
            }
        ]
        self.spells_lvl_1 = {
            "slot_number": 0,
            "spells": []
        }
        self.spells_lvl_2 = {
            "slot_number": 0,
            "spells": []
        }
        self.spells_lvl_3 = {
            "slot_number": 0,
            "spells": []
        }
        self.spells_lvl_4 = {
            "slot_number": 0,
            "spells": []
        }
        self.spells_lvl_5 = {
            "slot_number": 0,
            "spells": []
        }
        self.spells_lvl_6 = {
            "slot_number": 0,
            "spells": []
        }
        self.spells_lvl_7 = {
            "slot_number": 0,
            "spells": []
        }
        self.spells_lvl_8 = {
            "slot_number": 0,
            "spells": []
        }
        self.spells_lvl_9 = {
            "slot_number": 0,
            "spells": []
        }

    def attacks_string_to_display_string(self):
        """Changes a string from
         [Bite;Melee;6;one creature;reach 5ft;10 (2d6 + 3) piercing damage;effect on hit];[....];[]
         to a displayable string of all available attacks"""
        resulting_string = ""
        attacks = str(self.attacks).split(':')
        for attack in attacks:
            attack = attack[1:-1]
            attack_details = attack.split(';')
            resulting_string += "\n\t" + attack_details[0] + " " + attack_details[1] + "\n"
            resulting_string += "\t\tHit Bonus: " + attack_details[2] + "\n\t\tTarget: " + attack_details[3]
            resulting_string += "\n\t\tDamage: " + attack_details[4]
            if attack_details[5] is not '':
                resulting_string += "\n\t\tOn Hit: " + attack_details[5]
        return resulting_string

    def actions_dictionary_to_string(self):
        """Returns a string from dictionaries made of items with name / description ready to print"""
        resulting_string = ['\t' + item["name"] + "\n\t\t" + item["description"] + "\n" for item in self.actions]
        return '\n'.join(resulting_string)

    def traits_dictionary_to_string(self):
        """Returns a string from dictionaries made of items with name / effect ready to print"""
        resulting_string = ['\t' + item["name"] + "\n\t\t" + item["effect"] for item in self.traits]
        return '\n'.join(resulting_string)

    def cli_display(self):
        """ Display monster's stats """
        print("Name: " + self.name)
        print("Type: " + self.monster_type)
        print("Size: " + self.size)
        print("Alignment: " + self.alignment)
        print("Hit Points: " + str(self.hit_points) + ", Hit Dice: " + self.hit_dice)
        print("AC: " + str(self.armor_class))
        print("Passive Perception: " + str(self.passive_perception))

        if '' not in self.damage_immunities:
            print("Damage Immunities: " + ", ".join(self.damage_immunities))
        if '' not in self.damage_resistances:
            print("Damage Resistances: " + ", ".join(self.damage_resistances))
        if '' not in self.condition_immunities:
            print("Condition Immunities:" + ", ".join(self.condition_immunities))

        print('Attributes:')
        for attribute, value in self.attributes.items():
            print('\t' + attribute + ': ' + str(value))

        # saving throws
        for attribute, value in self.saving_throws.items():
            if value > 0:
                print(attribute + ' Saving Throw: +' + str(value))

        if len(self.senses) > 0 and self.senses[0] != '':
            print("Senses: " + ", ".join(self.senses))
        if len(self.languages_spoken) > 0 and self.languages_spoken[0] != '':
            print("Languages spoken: " + ", ".join(self.languages_spoken))
        if len(self.languages_understood) > 0 and self.languages_understood[0] != '':
            print("Languages understood: " + ", ".join(self.languages_understood))

        # spells
        for attr, value in self.__dict__.items():
            if attr.startswith('spells_lvl_') and value['slot_number'] > 0:
                num = attr.split('_')[-1]
                print('Spell slots of level {}: {}'.format(num, value['slot_number']))
                print('Available spells of level {}: {}'.format(num, ', '.join(value['spells'])))

        print("Description:\n\t" + self.description.replace('. ', '.\n\t'))

        # actions
        if len(self.attacks) > 0:
            print("Attacks:" + self.attacks_string_to_display_string())
        if len(self.traits) > 0:
            print("Traits:\n" + self.traits_dictionary_to_string())
        if len(self.actions) > 0:
            print("Actions:\n" + self.actions_dictionary_to_string())
