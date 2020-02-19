import json

from pathfinder.races.PFHuman import PFHuman
from utils.utilities import generate_attributes


class PFCharacter:
    def __init__(self, name=None, random=False):
        if name is None:
            self.name = "Adventurer"
        else:
            self.name = name
        self.stats = {
            "Strength": 10,
            "Dexterity": 10,
            "Constitution": 10,
            "Intelligence": 10,
            "Wisdom": 10,
            "Charisma": 10
        }
        self.race = PFHuman()

        if random:
            self.stats = generate_attributes(1)

            self.race = self.roll_race()

    def export_to_json(self):
        character_dict = {
            "name ": self.name,
            "race": self.race.race_name,
            "stats": self.stats,
        }
        test = json.dumps(character_dict)
        return test

    def roll_race(self):
        return PFHuman()


if __name__ == "__main__":
    bob = PFCharacter()
    print(bob.export_to_json())
