from characters.character import Character


class TravellerCharacter(Character):
    """
        Class dealing with a character according to the core rulebook of traveller creation
    """
    def __init__(self, name: str):
        """
        Initializes the character
            @:param name: a string to be the name of the character
        """
        super().__init__()

        self.name = name
