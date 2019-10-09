from databases.dnd5_monster_db import get_monster_by_name, get_number_of_monsters_in_db, \
    get_all_monsters_names_from_db, get_all_monsters_names_by_type, get_random_monster
from utils.utilities import attacks_string_to_display_string


def cli_display(monster):
    if monster is None:
        print("There is no such monster")
        return
    print("Name: " + monster.name)
    print("Type: " + monster.monster_type)
    print("Size: " + monster.size)
    print("Alignment: " + monster.alignment)
    print("Hit Points: " + str(monster.hit_points) + ", Hit Dice: " + monster.hit_dice)
    print("AC: " + str(monster.armor_class))
    print("Passive Perception: " + str(monster.passive_perception))

    if len(monster.damage_immunities) > 0 and monster.damage_immunities[0] != '':
        print("Damage Immunities: " + ", ".join(monster.damage_immunities))
    if len(monster.damage_resistances) > 0 and monster.damage_resistances[0] != '':
        print("Damage Resistances: " + ", ".join(monster.damage_resistances))
    if len(monster.condition_immunities) > 0 and monster.condition_immunities[0] != '':
        print("Condition Immunities :" + ", ".join(monster.condition_immunities))

    print("Attributes:\n\tStrength: " + str(monster.attributes["Strength"]) + "\n\tDexterity: " +
          str(monster.attributes["Dexterity"]) + "\n\tConstitution: " + str(monster.attributes["Constitution"]) +
          "\n\tIntelligence: " + str(monster.attributes["Intelligence"]) + "\n\tWisdom: " +
          str(monster.attributes["Wisdom"]) + "\n\tCharisma: " + str(monster.attributes["Charisma"]))

    if monster.saving_throws["Strength"] > 0 :
        print("Strength Saving Throw: +" + str((monster.saving_throws["Strength"])))
    if monster.saving_throws["Dexterity"] > 0 :
        print("Dexterity Saving Throw: +" + str((monster.saving_throws["Strength"])))
    if monster.saving_throws["Constitution"] > 0 :
        print("Constitution Saving Throw: +" + str((monster.saving_throws["Constitution"])))
    if monster.saving_throws["Intelligence"] > 0 :
        print("Intelligence Saving Throw: +" + str((monster.saving_throws["Intelligence"])))
    if monster.saving_throws["Wisdom"] > 0 :
        print("Wisdom Saving Throw: +" + str((monster.saving_throws["Wisdom"])))
    if monster.saving_throws["Charisma"] > 0 :
        print("Charisma Saving Throw: +" + str((monster.saving_throws["Charisma"])))

    if len(monster.senses) > 0 and monster.senses[0] != '':
        print("Senses: " + ", ".join(monster.senses))
    if len(monster.languages_spoken) > 0 and monster.languages_spoken[0] != '':
        print("Languages spoken: " + ", ".join(monster.languages_spoken))
    if len(monster.languages_understood) > 0 and monster.languages_understood[0] != '':
        print("Languages understood: " + ", ".join(monster.languages_understood))
    if monster.spells_lvl_1["slot_number"] > 0:
        print("Spell slots of level 1: " + str(monster.spells_lvl_1["slot_number"]))
        print("Available spells of level 1: " + ", ".join(monster.spells_lvl_1["spells"]))
    if monster.spells_lvl_2["slot_number"] > 0:
        print("Spell slots of level 2: " + str(monster.spells_lvl_2["slot_number"]))
        print("Available spells of level 2: " + ", ".join(monster.spells_lvl_2["spells"]))
    if monster.spells_lvl_3["slot_number"] > 0:
        print("Spell slots of level 3: " + str(monster.spells_lvl_3["slot_number"]))
        print("Available spells of level 3: " + ", ".join(monster.spells_lvl_3["spells"]))
    if monster.spells_lvl_4["slot_number"] > 0:
        print("Spell slots of level 4: " + str(monster.spells_lvl_4["slot_number"]))
        print("Available spells of level 4: " + ", ".join(monster.spells_lvl_4["spells"]))
    if monster.spells_lvl_5["slot_number"] > 0:
        print("Spell slots of level 5: " + str(monster.spells_lvl_5["slot_number"]))
        print("Available spells of level 5: " + ", ".join(monster.spells_lvl_5["spells"]))
    if monster.spells_lvl_6["slot_number"] > 0:
        print("Spell slots of level 6: " + str(monster.spells_lvl_6["slot_number"]))
        print("Available spells of level 6: " + ", ".join(monster.spells_lvl_6["spells"]))
    if monster.spells_lvl_7["slot_number"] > 0:
        print("Spell slots of level 7: " + str(monster.spells_lvl_7["slot_number"]))
        print("Available spells of level 7: " + ", ".join(monster.spells_lvl_7["spells"]))
    if monster.spells_lvl_8["slot_number"] > 0:
        print("Spell slots of level 8: " + str(monster.spells_lvl_8["slot_number"]))
        print("Available spells of level 8: " + ", ".join(monster.spells_lvl_8["spells"]))
    if monster.spells_lvl_9["slot_number"] > 0:
        print("Spell slots of level 9: " + str(monster.spells_lvl_9["slot_number"]))
        print("Available spells of level 9: " + ", ".join(monster.spells_lvl_9["spells"]))
    print("Description:\n\t" + monster.description.replace('. ', '.\n\t'))
    if len(monster.attacks) > 0:
        print("Attacks:" + attacks_string_to_display_string(monster.attacks))


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
            cli_display(monster)
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
        cli_display(get_random_monster())