

class Character:
    """
        Base class for characters in general, regardless of system
        Will probably contain more info later
    """
    def __init__(self):
        self.name = ""

    def rename(self, name: str):
        """
            Change character name
            :param name: a str for the character
            :return: nothing
        """
        self.name = name
