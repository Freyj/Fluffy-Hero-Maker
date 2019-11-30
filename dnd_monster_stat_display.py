from databases.dnd5.dnd5_monster_db import get_monster_by_name, get_number_of_monsters_in_db, \
    get_all_monsters_names_from_db, get_all_monsters_names_by_type, get_random_monster


def dnd_monster_stat_display():
    print("Type 1 for finding a monster by name, Type 2 to find the list of monsters in the database, Type 3 to find "
          "monsters of a type, type 4 for a random monster")
    choice = input()
    if choice is "1":
        print("Please give the name of the monster you are looking for:")
        monster_name = input().strip()
        monster = get_monster_by_name(monster_name)
        if monster is None:
            print("No monster found with name: " + monster_name)
        else:
            monster.cli_display()
    if choice is "2":
        print("The database contains " + str(get_number_of_monsters_in_db()) + " monsters.")
        print("The database contains the following monsters: ")
        print(", ".join(get_all_monsters_names_from_db()))
    if choice is "3":
        print("Choose a type of monster")
        monster_type = input().strip()
        print("The database contains the following monsters of type " + monster_type + ".")
        print(", ".join(get_all_monsters_names_by_type(monster_type)))
    if choice is "4":
        print("Find a random monster")
        get_random_monster().cli_display()
