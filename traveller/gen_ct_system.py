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

        self.calc_size()
        self.calc_atmosphere()

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
            self.atmosphere = "0"
        if self.size == "A":
            size = 10
        else:
            size = int(self.size)
        roll = sum_roll_dice(6, 2) - 7 + size
        if roll < 0:
            self.atmosphere = "0"
        else:
            self.atmosphere = hex(roll)[2:].upper()


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
