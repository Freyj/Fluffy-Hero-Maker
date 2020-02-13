from utils.dice_roller import roll_die, sum_roll_dice


class CTHex:
    def __init__(self, world_dm=0):
        self.name = ""
        self.hex = ""
        self.has_world = False
        self.has_gas_giant = True
        self.starport = ""
        self.has_naval_base = False
        self.has_scout_base = False

        self.calc_world_presence(dm=world_dm)
        self.calc_gas_giant_presence()
        if self.has_world:
            self.calc_starport_type()
            self.calc_naval_base()
            self.calc_scout_base()

        if self.has_world:
            self.world = CTWorld(self)

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
        if roll > 9:
            self.has_gas_giant = False

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
            dm = -1
        elif self.starport == "B":
            dm = -2
        elif self.starport == "A":
            dm = -3
        if self.starport not in ["E", "X"]:
            roll = sum_roll_dice(6, 2)
            if roll > 6:
                self.has_scout_base = True


class CTWorld:
    def __init__(self, hexagon: CTHex):
        self.name = ""
        self.hex = hexagon
        self.size = "0"
        self.atmosphere = "0"
        self.hydrography = "0"
        self.population = "0"
        self.government = "0"
        self.law_level = "0"
        self.technological_level = "0"
        self.classifications = []

        self.calc_stats()

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
            self.hydrography = "0"
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


def random_ct_world_gen():
    hexagon = CTHex()
    world = CTWorld(hexagon)
    return world


if __name__ == "__main__":
    running = True
    while running:
        hexagon = CTHex()
        world = CTWorld(hexagon)
        print(world.__dict__)
        print(hexagon.__dict__)
        x = input("Quit on Q\n")
        if x == "Q":
            running = False
