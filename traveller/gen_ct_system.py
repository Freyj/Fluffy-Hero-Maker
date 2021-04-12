from traveller.consts_trav import STARPORT_TYPES, WORLD_SIZES, ATMOSPHERE_TYPES, HYDROGRAPHY, POPULATION, \
    GOVERNMENT_TYPES, TECH_LEVELS, LAW_LEVELS
from utils.dice_roller import roll_die, sum_roll_dice


class CTHex:
    def __init__(self, name="", world_dm=0, hex_position=""):
        self.name = name
        self.hex = hex_position
        self.has_world = False
        self.has_gas_giant = False
        self.gas_giant_number = 0
        self.starport = "X"
        self.has_naval_base = False
        self.has_scout_base = False
        self.worlds = []

        self.calc_world_presence(dm=world_dm)
        if self.has_world:
            self.calc_gas_giant_presence()
            self.calc_starport_type()
            self.calc_naval_base()
            self.calc_scout_base()
            if self.has_gas_giant:
                roll = roll_die(3)
                self.gas_giant_number = roll
            roll = roll_die(3)
            for _ in range(roll):
                self.worlds.append(CTWorld(self))

    def description_str(self):
        result_str = "Name: {n}\nHex: {h}".format(n=self.name, h=self.hex)
        if self.has_scout_base:
            result_str += "\nContains a Scout Base."
        if self.has_naval_base:
            result_str += "\nContains a Naval Base."
        if self.starport != "":
            result_str += "\nStarport {s}: {ds}".format(s=self.starport, ds=describe_starport(self.starport))
        if self.has_gas_giant:
            result_str += "\nContains {nb} gas giant(s).".format(nb=self.gas_giant_number)
        if self.has_world:
            result_str += "\nWorlds:"
            for world in self.worlds:
                result_str += "\n\t" + world.description_str()
        return result_str

    def calc_world_presence(self, dm=0):
        """
            Worlds have a 50% chance of existing in a hex in most cases
            :param dm modifier is for cases in which sectors are more densily with worlds
        """
        roll = roll_die(6) + dm
        if roll > 3:
            self.has_world = True

    def calc_gas_giant_presence(self):
        """
            Gas giants are common
        """
        roll = sum_roll_dice(6, 2)
        if roll < 10:
            self.has_gas_giant = True

    def calc_starport_type(self):
        """
            Calculates the type of starport
        """
        roll = sum_roll_dice(6, 2)
        if roll in [2, 3, 4]:
            self.starport = "A"
        elif roll in [5, 6]:
            self.starport = "B"
        elif roll in [7, 8]:
            self.starport = "C"
        elif roll == 9:
            self.starport = "D"
        elif roll in [10, 11]:
            self.starport = "E"
        elif roll == 12:
            self.starport = "X"

    def calc_naval_base(self):
        """
            Caculates the presence of a naval base
        """
        if self.starport not in ["C", "D", "E", "X"]:
            roll = sum_roll_dice(6, 2)
            if roll > 7:
                self.has_naval_base = True

    def calc_scout_base(self):
        """
            Calculates the presence of a scout base
        """
        dm = 0
        if self.starport == "C":
            dm += -1
        elif self.starport == "B":
            dm += -2
        elif self.starport == "A":
            dm += -3
        if self.starport not in ["E", "X"]:
            roll = sum_roll_dice(6, 2) + dm
            if roll > 6:
                self.has_scout_base = True


def describe_starport(starport_letter: str):
    res = ""
    if starport_letter in ["A", "B", "C", "D", "E", "X"]:
        res = STARPORT_TYPES[starport_letter]
    else:
        print("Error in starport letter")
    return res


class CTWorld:
    def __init__(self, hexagon: CTHex, name=None):
        if name is None:
            self.name = "Unnamed World"
        else:
            self.name = name
        self.hex = hexagon

        self.atmosphere = "0"
        self.government = "0"
        self.hydrography = "0"
        self.law_level = "0"
        self.population = "0"
        self.size = "0"
        self.technological_level = "0"
        self.classifications = []

        self.atmosphere_desc = ""
        self.government_desc = ""
        self.hydrography_desc = ""
        self.law_level_desc = ""
        self.population_desc = ""
        self.size_desc = ""
        self.starport_desc = ""
        self.technological_level_desc = ""

        self.calc_stats()
        self.add_descs()

    def add_descs(self):
        self.starport_desc = STARPORT_TYPES[self.hex.starport]
        self.size_desc = WORLD_SIZES[self.size]
        self.atmosphere_desc = ATMOSPHERE_TYPES[self.atmosphere]
        self.hydrography_desc = HYDROGRAPHY[self.hydrography]
        self.population_desc = POPULATION[self.population]
        self.government_desc = GOVERNMENT_TYPES[self.government]
        self.law_level_desc = LAW_LEVELS[self.law_level]
        self.technological_level_desc = TECH_LEVELS[self.technological_level]

    def calc_stats(self):
        self.calc_size()
        self.calc_atmosphere()
        self.calc_hydrography()
        self.calc_population()
        self.calc_government()
        self.calc_law_level()
        self.calc_technological_level()
        self.get_trade_classification()

    def calc_size(self):
        """
            Calculates the world size
        """
        roll = sum_roll_dice(6, 2) - 2
        self.size = hex(roll)[2:].upper()

    def calc_atmosphere(self):
        """
            Calculates the atmosphere of the world
        """
        if self.size == "0":
            size = 0
        elif self.size == "A":
            size = 10
        else:
            size = int(self.size)
        roll = sum_roll_dice(6, 2) - 7 + size
        if roll < 0:
            roll = 0
        elif roll > 12:
            roll = 12
        self.atmosphere = hex(roll)[2:].upper()

    def calc_hydrography(self):
        """
            Calculates planetary hydrographic percentage
        """
        if self.size == 0:
            self.hydrography = "0"
        dm = 0
        if self.atmosphere in ["0", "1", "A", "B", "C"]:
            dm = -4
        else:
            dm = int(self.atmosphere)
        roll = sum_roll_dice(6, 2) - 7 + dm
        if roll < 0:
            roll = 0
        if roll > 10:
            roll = 10
        hex_trans = hex(roll)[2:].upper()
        if len(hex_trans) > 1:
            hex_trans = hex_trans[len(hex_trans) - 1]
        self.hydrography = hex_trans

    def calc_population(self):
        roll = sum_roll_dice(6, 2) - 2
        self.population = hex(roll)[2:].upper()

    def calc_government(self):
        if self.population == "A":
            pop = 10
        else:
            pop = str(self.population)
        roll = sum_roll_dice(6, 2) - 7 + int(pop)
        if roll < 0:
            roll = 0
        elif roll > 13:
            roll = 13
        self.government = hex(roll)[2:].upper()

    def calc_law_level(self):
        if self.government == "A":
            gov = 10
        elif self.government == "B":
            gov = 11
        elif self.government == "C":
            gov = 12
        elif self.government == "D":
            gov = 13
        else:
            gov = int(self.government)
        roll = sum_roll_dice(6, 2) - 7 + int(gov)
        if roll < 0:
            roll = 0
        elif roll > 10:
            roll = 10
        hex_trans = hex(roll)[2:].upper()
        if len(hex_trans) > 1:
            hex_trans = hex_trans[len(hex_trans) - 1]
        self.law_level = hex_trans

    def calc_technological_level(self):
        dm = 0
        if self.hex.starport == "A":
            dm += 6
        elif self.hex.starport == "B":
            dm += 4
        elif self.hex.starport == "C":
            dm += 2
        elif self.hex.starport == "X":
            dm -= 4

        if self.size in ["0", "1"]:
            dm += 2
        elif self.size in ["2", "3", "4"]:
            dm += 1

        if self.atmosphere in ["0", "1", "2", "3", "A", "B", "C", "D", "E"]:
            dm += 1

        if self.hydrography == "9":
            dm += 1
        elif self.hydrography == "A":
            dm += 2

        if self.population in ["1", "2", "3", "4", "5"]:
            dm += 1
        elif self.population == "9":
            dm += 2
        elif self.population == "A":
            dm += 4

        if self.government == "0":
            dm += 1
        elif self.government == "5":
            dm += 1
        elif self.government == "D":
            dm -= 2

        if self.government == "A":
            gov = 10
        elif self.government == "B":
            gov = 11
        elif self.government == "C":
            gov = 12
        elif self.government == "D":
            gov = 13
        else:
            gov = self.government
        roll = roll_die(6) + int(gov) + dm
        if roll < 0:
            roll = 0
        # arbitrary max tl 16
        hex_trans = hex(roll)[2:].upper()
        if len(hex_trans) > 1:
            hex_trans = hex_trans[len(hex_trans) - 1]
        self.technological_level = hex_trans

    def get_trade_classification(self):
        classifications = []
        if self.atmosphere in ["4", "5", "6", "7", "8", "9"]:
            if self.hydrography in ["4", "6", "7", "8"]:
                if self.population in ["5", "6", "7"]:
                    classifications.append("Agricultural")
        if self.atmosphere in ["0", "1", "2", "3"]:
            if self.hydrography in ["0", "1", "2", "3"]:
                if self.population in ["6", "7", "8", "9", "A"]:
                    classifications.append("Non-Agricultural")
        if self.atmosphere in ["0", "1", "2", "3", "4", "7", "9"]:
            if self.population in ["9", "A"]:
                classifications.append("Industrial")
        if self.population in ["0", "1", "2", "3", "4", "5", "6"]:
            classifications.append("Non-Industrial")
        if self.atmosphere in ["6", "8"]:
            if self.population in ["6", "7", "8"]:
                if self.government in ["4", "5", "6", "7", "8", "9"]:
                    classifications.append("Rich")
        if self.atmosphere in ["2", "3", "4", "5"]:
            if self.hydrography in ["0", "1", "2", "3"]:
                classifications.append("Poor")
        if self.hydrography == "A":
            classifications.append("Water World")
        if self.hydrography == "0":
            if self.atmosphere in ["2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C"]:
                classifications.append("Desert World")
        if self.atmosphere == "0":
            classifications.append("Vacuum World")
        if self.size == "0":
            classifications.append("Asteroid Belt")
        if self.atmosphere in ["0", "1"]:
            if self.hydrography != "0":
                classifications.append("Ice-capped")
        self.classifications = classifications

    def description_str(self):
        result_str = "{n} at hex {h}".format(n=self.name, h=self.hex.hex)
        result_str += "\n\t\tTechnological Level: {tl}, {tltr}".format(tl=self.technological_level,
                                                                       tltr=TECH_LEVELS[self.technological_level])
        classifications = ""
        for i in self.classifications:
            classifications += i + ", "
        classifications = classifications[:-2]
        result_str += "\n\t\tTrade Classifications: {tc}".format(tc=classifications)
        result_str += "\n\t\tSize: {s}\n\t\tAtmosphere: {at}".format(s=WORLD_SIZES[self.size],
                                                                     at=ATMOSPHERE_TYPES[self.atmosphere])
        result_str += "\n\t\tHydrography: {h}\n\t\tPopulation: {p}".format(h=HYDROGRAPHY[self.hydrography],
                                                                           p=POPULATION[self.population])
        result_str += "\n\t\tGovernment Type: {g}".format(g=GOVERNMENT_TYPES[self.government])
        result_str += "\n\t\tLaw Level: {ll}".format(ll=LAW_LEVELS[self.law_level])
        return result_str


def random_ct_world_gen(name=None):
    hexagon = CTHex(hex_position="0101", name="Test")
    world = CTWorld(hexagon, name=name)
    return world


if __name__ == "__main__":
    running = True
    while running:
        x = input("Quit on Q, give hex position\n")
        if x == "Q":
            running = False
        else:
            hexagon = CTHex(hex_position=x, name="Test")
            print(hexagon.description_str())
