from traveller.CTCharacter import CTCharacter


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
            ct_char.read_history()
            print(ct_char.char_details())
            save = input("Do you want to save file? Anything else than No will produce a file of this name\n")
            if save != "No" and save != "":
                ct_char.save_character(save)
