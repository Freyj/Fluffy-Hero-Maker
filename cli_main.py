from databases.dnd5_races_db import insert_dnd5_race, look_for_race_by_name
from databases.dnd5_db import create_dnd5_db, drop_all_tables


import argparse

from dnd_character_creator import dnd_character_creation
from dnd_monster_stat_display import dnd_monster_stat_display
from dnd_spell_display import dnd_spell_display

# Debug value to empty db on each launch
DEBUG = True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Utilities software for role-playing games.')
    not_finished = True
    if DEBUG:
        drop_all_tables()
    dnd5_db = create_dnd5_db()
    while not_finished:
        print("Input wanted tool: 1 for a dnd5 character creator, 2 for dnd5 monster stats, 3 for spell finder")
        choice = input()  # for the moment we have no choice
        if choice == "1":
            dnd_character_creation()
        if choice == "2":
            dnd_monster_stat_display()
        if choice == "3":
            dnd_spell_display()
        # loop on other creation
        print("Do you want to continue?")
        again = input()
        if again != "yes":
            not_finished = False
