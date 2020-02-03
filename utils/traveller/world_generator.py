

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
    for i in list_components:
        print(i)
    name = list_components[0]
    hex_location = list_components[1]
    starport_quality = list_components[2][0]
    size = list_components[3][1]


if __name__ == "__main__":
    read_world_profile("Cogri 0101 CA6A643–9 N Ri Wa A")
