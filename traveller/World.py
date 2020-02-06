import json

from utils.dice_roller import sum_roll_dice, roll_die

WORLD_SIZE_INFO = {
    '0': {
        "size": 800,
        "gravity": 0
    },
    'A': {
        "size": 16000,
        "gravity": 1.4
    }
}

ATMOSPHERE_INFO = {
    '0': {
        'Name': 'None',
        'Pressure': "0.00",
        'Survival Gear': "Vacc Suit"
    },
    '1': {
        'Name': 'Trace',
        'Pressure': "0.001 to 0.09",
        "Survival Gear": "Vacc Suit"
    },
    '2': {
        'Name': 'Very Thin, Tainted',
        'Pressure': "0.1 to 0.42",
        "Survival Gear": "Respirator, Filter"
    },
    '3': {
        'Name': 'Very Thin',
        'Pressure': "0.1 to 0.42",
        "Survival Gear": "Respirator"
    },
    '4': {
        'Name': 'Thin, Tainted',
        'Pressure': "0.43 to 0.7",
        "Survival Gear": "Filter"
    },
    '5': {
        'Name': 'Thin',
        'Pressure': "0.43 to 0.7",
        "Survival Gear": ""
    },
    '6': {
        'Name': 'Standard',
        'Pressure': "0.71 to 1.49",
        "Survival Gear": ""
    },
    '7': {
        'Name': 'Standard, Tainted',
        'Pressure': "0.71 to 1.49",
        "Survival Gear": "Filter"
    },
    '8': {
        'Name': 'Dense',
        'Pressure': "1.5 to 2.49",
        "Survival Gear": ""
    },
    '9': {
        'Name': 'Dense, Tainted',
        'Pressure': "1.5 to 2.49",
        "Survival Gear": "Filter"
    },
    'A': {
        'Name': 'Exotic',
        'Pressure': "Varies",
        "Survival Gear": "Vacc Suit"
    },
    'B': {
        'Name': 'Corrosive',
        'Pressure': "Varies",
        "Survival Gear": "Vacc Suit"
    },
    'C': {
        'Name': 'Insidious',
        'Pressure': "Varies",
        "Survival Gear": "Vacc Suit"
    },
    'D': {
        'Name': 'Dense, High',
        'Pressure': "2.5+",
        "Survival Gear": ""
    },
    'E': {
        'Name': 'Thin, Low',
        'Pressure': "0.5 or less",
        "Survival Gear": ""
    },
    'F': {
        'Name': 'Unusual',
        'Pressure': "Varies",
        "Survival Gear": "Varies"
    }
}

TEMPERATURE_INFO = [
    {"Frozen": "-51"},
    {"Cold": "-51 to 0"},
    {"Temperate": "0 to 30"},
    {"Hot": "31 to 80"},
    {"Roasting": "81"}
]


class World:
    """
        Class describing worlds in the Traveller game
    """

    def __init__(self, name: str):
        self.name = name
        self.hex_location = ""
        self.starport = ""
        self.size_code = ""
        self.gravity = 0
        self.size = 0
        self.atmosphere = ""
        self.habitable_zone = 0  # -1 if cold edge, 0 if normal, +1 if hot edge
        self.temperature = {}

    def export_json(self):
        return json.dump(self, indent=2, separators=(',', ': '))

    def create_uwp(self):
        return "{name} {hex_location}".format(name=self.name,
                                              hex_location=self.hex_location)

    def world_short_display(self):
        print("World Name: {name}\nWorld Location:{col} {row}".format(name=self.name,
                                                                      col=self.hex_location[:2],
                                                                      row=self.hex_location[2:4]))
        print("Size: {size_code}\nStarport: {sp}".format(sp=self.starport,
                                                         size_code=self.size_code))
        print("Atmosphere: {at}\nTemperature: {tp}".format(at=ATMOSPHERE_INFO[self.atmosphere]["Name"],
                                                           tp=self.temperature))

    def world_longer_display(self):
        print("World Name: {name}\nWorld Location:{col} {row}".format(name=self.name,
                                                                      col=self.hex_location[:2],
                                                                      row=self.hex_location[2:4]))
        print("Size category: ({size_code}) {km}km, Gravity: {g}g\nStarport: {sp}".format(sp=self.starport,
                                                                                               size_code=self.size_code,
                                                                                               km=self.size,
                                                                                               g=self.gravity))
        print("Atmosphere: {at}\nGravity: {grav}\nTemperature: {tp}".format(at=ATMOSPHERE_INFO[self.atmosphere]["Name"],
                                                                            grav=ATMOSPHERE_INFO[self.atmosphere]["Pressure"],
                                                                            tp=self.temperature))

    def get_world_size_and_gravity(self):
        """
            Returns the world size_code in km and the
            surface gravity
            :return: int and float
        """
        world_size = 0
        gravity = 0
        if self.size_code == '0':
            world_size = 800
        elif self.size_code == '1':
            world_size = 1600
            gravity = 0.05
        elif self.size_code == '2':
            world_size = 3200
            gravity = 0.15
        elif self.size_code == '3':
            world_size = 4800
            gravity = 0.25
        elif self.size_code == '4':
            world_size = 6400
            gravity = 0.35
        elif self.size_code == '5':
            world_size = 8000
            gravity = 0.45
        elif self.size_code == '6':
            world_size = 9600
            gravity = 0.7
        elif self.size_code == '7':
            world_size = 11200
            gravity = 0.9
        elif self.size_code == '8':
            world_size = 12800
            gravity = 1.0
        elif self.size_code == '9':
            world_size = 14400
            gravity = 1.25
        elif self.size_code == 'A':
            world_size = 16000
            gravity = 1.4
        return world_size, gravity

    def is_low_grav(self):
        """
            Checks if the world is low gravity
            :return: True if the gravity is equal or lower to 0.75
        """
        if self.gravity > 0.75:
            return False
        else:
            return True

    def roll_for_habitable_zone(self):
        habitable_roll = roll_die(3)
        if habitable_roll == 2:
            self.habitable_zone = -1
        else:
            self.habitable_zone = habitable_roll

    def calculate_temperature_dm(self):
        """
            Calculate dice modifier for temperature roll
            :return:  a signed int
        """
        res = 0
        if self.habitable_zone == 1:
            res += 4
        elif self.habitable_zone == -1:
            res -= 4
        if self.atmosphere == '0' or self.atmosphere == '1':
            pass
        if self.atmosphere == '2' or self.atmosphere == '3':
            res -= 2
        if self.atmosphere == '4' or self.atmosphere == '5' or self.atmosphere == 'E':
            res -= 1
        if self.atmosphere == '6' or self.atmosphere == '7':
            pass
        if self.atmosphere == '8' or self.atmosphere == '9':
            res += 1
        if self.atmosphere == 'A' or self.atmosphere == 'D' or self.atmosphere =='F':
            res += 2
        if self.atmosphere == 'B' or self.atmosphere == 'C':
            res += 6
        return res

    def roll_for_temperature(self):
        result = sum_roll_dice(6, 2) + self.calculate_temperature_dm()
        if result <= 2:
            self.temperature = TEMPERATURE_INFO[0]
        elif result == 3 or result == 4:
            self.temperature = TEMPERATURE_INFO[1]
        elif 5 <= result <= 9:
            self.temperature = TEMPERATURE_INFO[2]
        elif result == 10 or result == 11:
            self.temperature = TEMPERATURE_INFO[3]
        elif result >= 12:
            self.temperature = TEMPERATURE_INFO[4]


def generate_random_world(name: str, hex_location: str):
    """
        Generates a random world according to Traveller SRD rules
        :param name:
        :param hex_location
        :return:
    """
    world = World(name)
    world.hex_location = hex_location
    world.starport = roll_for_starport()
    world.size_code = roll_for_world_size()
    world.size, world.gravity = world.get_world_size_and_gravity()
    world.atmosphere = roll_for_atmosphere(world)
    world.roll_for_habitable_zone()
    world.roll_for_temperature()

    return world


def roll_for_starport():
    """
        Returns the starport code from a random roll
        :return: [XABCDE]
    """
    result = sum_roll_dice(6, 2)
    if result == 2:
        return 'X'
    elif result == 3 or result == 4:
        return 'E'
    elif result == 5 or result == 6:
        return 'D'
    elif result == 7 or result == 8:
        return 'C'
    elif result == 9 or result == 10:
        return 'B'
    elif result > 10:
        return 'A'


def roll_for_world_size():
    """
        Returns the size_code code from a random roll
        :return: [0123456789A]
    """
    result = roll_die(10)
    if result < 10:
        return str(result)
    else:
        return 'A'


def roll_for_atmosphere(world):
    """
        Rolls according to the SRD rules for atmosphere of a world
        "A planet’s Atmosphere is generated by rolling 2d6–7 and
        adding the planet’s Size"
        :param world:
        :return: [0123456789ABCDEF]
    """
    if world.size_code == 'A':
        code = 10
    else:
        code = int(world.size_code)
    result = sum_roll_dice(6, 2) - 7 + code
    if result < 0:
        result = 0
    if result < 10:
        return str(result)
    elif result == 10:
        return 'A'
    elif result == 11:
        return 'B'
    elif result == 12:
        return 'C'
    elif result == 13:
        return 'D'
    elif result == 14:
        return 'E'
    elif result == 15:
        return 'F'
