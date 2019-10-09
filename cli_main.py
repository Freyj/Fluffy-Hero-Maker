from databases.db_populate import delete_all_data, create_database, initialize_all_data

import argparse

from dnd_character_creator import dnd_character_creation
from dnd_monster_stat_display import dnd_monster_stat_display
from dnd_spell_display import dnd_spell_display


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Utilities software for role-playing games.')
    parser.add_argument("-d", help="activate debug mode and delete all tables at launch")
    not_finished = True
    args = parser.parse_args()
    if args.d:
        delete_all_data()
        create_database()
        initialize_all_data()
    while not_finished:
        print("Input wanted tool: 1 for a dnd5 character creator, 2 for dnd5 monster stats, 3 for spell finder")
        choice = input()
        if choice == "1":
            dnd_character_creation()
        if choice == "2":
            dnd_monster_stat_display()
        if choice == "3":
            dnd_spell_display()
        # loop
        print("Do you want to continue?")
        again = input()
        if again != "yes":
            not_finished = False
