import json


class World:
    """
        Class describing worlds in the Traveller game
    """
    def __init__(self, name: str):
        self.name = name
        self.hex_location = ""

    def export_json(self):
        return json.dumps(self, indent=2, separators=(',', ': '))

    def create_uwp(self):
        return "{name} {hex_location}".format(name=self.name,
                                              hex_location=self.hex_location)
