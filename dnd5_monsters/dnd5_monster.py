from utils.utilities import list_to_str


class DnD5Monster:
    def __init__(self, name):
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
        self.damage_immunities = ""
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
