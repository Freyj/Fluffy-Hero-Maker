from traveller.World import generate_random_world, roll_for_starport
from utils.dice_roller import sum_roll_dice


def read_world_profile(uwp: str):
    """
        Reads a Universal World Profile and details the information from the world
        :param uwp:
            Traveller describes planets with the Universal World Profile, a
            single line of code such as:
            Cogri 0101 CA6A643–9 N Ri Wa A
            The first component is the name. The second component (four
            digit number) is the hex location (column and row).
            The string of digits following that denote, in order:
            • Starport quality
            • Size
            • Atmosphere Type
            • Hydrographic percentage
            • Population
            • Government Type
            • Law Level
            • (hyphen)
            • Tech Level
            The next component marks any bases present on the world
            – examples include N for Naval Base or S for Scout Base.
            This is followed by any Trade Codes for the planet.
            The travel zone for the system is next – A = Amber Zone, R = Red
            Zone. If no code is given then the world is either unclassified or
            a Green Zone.
        :return: a world object
    """
    list_components = uwp.split(" ")
    print(uwp)
    print(len(uwp))
    for i in list_components:

        print(i)
    name = list_components[0]
    hex_location = list_components[1]
    hex_col = hex_location[:2]
    hex_row = hex_location[2:]
    starport_quality = list_components[2][0]
    size = list_components[2][1]
    atmosphere_type = list_components[2][2]
    hydrographic_percentage = list_components[2][3]
    population = list_components[2][4]
    government_type = list_components[2][5]
    law_level = list_components[2][6]
    tech_level = list_components[2][7]

    bases_present = list_components[3]
    trade_code = list_components[4]


if __name__ == "__main__":
    # read_world_profile("Cogri 0101 CA6A643–9 N Ri Wa A")
    world = generate_random_world("Corgi", "0101")
    print("***********************************************")
    print(world.world_short_display())
    print("***********************************************")
    print(world.world_longer_display())
