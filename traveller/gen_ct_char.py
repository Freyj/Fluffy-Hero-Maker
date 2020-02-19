from traveller.CTCharacter import CTCharacter
from utils.dice_roller import roll_die


def generate_traveller_character():
    """
        Runs a classic traveller character generation in CLI
    """
    running = True
    while running:
        ct_char = CTCharacter()
        choice = ""
        print("UPP: {upp}".format(upp=ct_char.get_upp()))
        while choice not in ["Navy", "Marines", "Army", "Others", "Scouts", "Merchants", "Q"]:
            choice = input("Choose service to try for: (Navy, Marines, Army, Scouts, Merchants, Others. Q to quit.)\n")
        if choice == "Q":
            running = False
        else:
            ct_char.choose_service(choice)
            stays_in_service = True
            while ct_char.survived and stays_in_service:
                ct_char.term()
                if ct_char.survived:
                    if ct_char.reenlisting == 1:
                        reenlist = "y"
                    elif ct_char.reenlisting == -1:
                        reenlist = "n"
                    else:
                        reenlist = ""
                    while reenlist not in ["y", "n"]:
                        reenlist = input("Again? y for yes, n for no\n")
                    if reenlist == "n":
                        stays_in_service = False
                else:
                    stays_in_service = False
            if ct_char.survived:
                ct_char.calc_muster_out()
            choice_name = input("Pick a name for the character\n")
            ct_char.name = choice_name
            ct_char.read_history()
            print(ct_char.char_details())
            save = input("Do you want to save file?  \n")
            if save == "y":
                ct_char.save_character(ct_char.name)


def random_classic_traveller_character(name: str, must_be_alive=False):
    """
        Produces a random character for classic traveller
        :param name: the name of the character
        :param must_be_alive: to forgo the rolls of characters that failed to
            survive their term
        :return: a CTCharacter object
    """
    valid_char = False
    while not valid_char:
        character = CTCharacter()
        choice_service = roll_die(6)
        services = ["Navy", "Marines", "Army", "Others", "Scouts", "Merchants"]
        character.choose_service(services[choice_service - 1], True)
        stays_in_service = True
        while character.survived and stays_in_service:
            character.term(automatic=True)
            if character.survived:
                if character.reenlisting == 0:
                    reenlist_roll = roll_die(2)
                    if reenlist_roll == 0:
                        stays_in_service = False
                elif character.reenlisting == -1:
                    stays_in_service = False
        if character.survived:
            character.calc_muster_out(automatic=True)
        if (must_be_alive and character.survived) or not must_be_alive:
            valid_char = True
        character.name = name
    return character


def random_classic_traveller_party_generator():
    """
        Produces a party of 4 random characters for classic traveller, all alive
        :return: an array of 4 CTCharacter objects
    """
    characters = []
    for i in range(4):
        character = random_classic_traveller_character("Member {i}".format(i=i))
        while not character.survived:
            character = random_classic_traveller_character("Member {i}".format(i=i))
        characters.append(character)
    return characters

