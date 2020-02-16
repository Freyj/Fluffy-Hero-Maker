from traveller.CTCharacter import CTCharacter
from utils.dice_roller import roll_die


def generate_traveller_character():
    running = True
    while running:
        ct_char = CTCharacter()
        choice = ""
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


def random_classic_traveller_character(name: str):
    character = CTCharacter()
    choice_service = roll_die(6)
    services = ["Navy", "Marines", "Army", "Others", "Scouts", "Merchants"]
    character.choose_service(services[choice_service - 1], True)
    stays_in_service = True
    while character.survived and stays_in_service:
        character.term(automatic=True)
        if character.survived:
            if character.reenlisting == 0:
                # reenlisting is less likely if character is older (for randomness, because players would be more
                # likely to leave service if the character is old)
                roll_size = 2
                if character.age > 36:
                    roll_size = 3
                elif character.age > 50:
                    roll_size = 4
                elif character.age > 60:
                    roll_size = 5
                reenlist_roll = roll_die(roll_size)
                if reenlist_roll != roll_size:
                    stays_in_service = False
            elif character.reenlisting == -1:
                stays_in_service = False
    if character.survived:
        character.calc_muster_out(automatic=True)
    character.name = name
    return character


def random_classic_traveller_party_generator():
    characters = []
    for i in range(4):
        character = random_classic_traveller_character("Member {i}".format(i=i))
        while not character.survived:
            character = random_classic_traveller_character("Member {i}".format(i=i))
        characters.append(character)
    return characters
