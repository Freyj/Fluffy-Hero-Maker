from characters.dnd5 import Dnd5Character
from databases.dnd5_backgrounds import insert_dnd5_background, get_all_background_names, get_background_by_name
from databases.dnd5_classes_db import insert_dnd5_classes, get_all_classes_names, look_for_class_by_name
from databases.dnd5_languages_db import get_all_languages, get_all_unrestricted_languages, insert_dnd5_language
from databases.dnd5_races_db import get_all_races_names, look_for_race_by_name, insert_dnd5_race
from dnd5_character.dnd5_constants import GENERATION_TYPES
from utils.utilities import is_valid_choice, list_to_str, dict_to_str, list_to_str_with_number_and_line


def cli_display(character):
    """Displays the character chosen in stdout through prints"""
    print("Name: " + character.name)
    print("Hit Points: " + str(character.hit_points))
    print("Race: " + character.race.name)
    print("Class: " + character.dnd_class.name)
    print("Background: " + character.background)
    print("Alignment: " + character.alignment)
    print("Size: " + character.size)
    print("Age: " + str(character.age))
    print("Vision: " + list_to_str(character.vision))

    # Todo: change this into a function for attributes str result (like saving throws)
    print("Attributes:\n\tStrength: "
          + str(character.attributes["Strength"]) + "(" + str(character.get_modifier("Strength")) + ")"
          + "\n\tDexterity: " + str(character.attributes["Dexterity"]) + "("
          + str(character.get_modifier("Dexterity")) + ")"
          + "\n\tConstitution: " + str(character.attributes["Constitution"])
          + "(" + str(character.get_modifier("Constitution")) + ")"
          + "\n\tIntelligence: " + str(character.attributes["Intelligence"])
          + "(" + str(character.get_modifier("Intelligence")) + ")"
          + "\n\tWisdom: " + str(character.attributes["Wisdom"]) + "("
          + str(character.get_modifier("Wisdom")) + ")"
          + "\n\tCharisma: " + str(character.attributes["Charisma"])
          + "(" + str(character.get_modifier("Charisma")) + ")")

    print("Saving Throws: " + character.saving_throws_to_str())
    language_string = "Languages: " + list_to_str(character.languages)
    print(language_string)
    skill_proficiency_string = "Skill proficiencies: " + list_to_str(character.skill_proficiencies)
    print(skill_proficiency_string)
    if len(character.tool_proficiencies) > 0:
        tool_proficiency_string = "Tool proficiencies: " + list_to_str(character.tool_proficiencies)
        print(tool_proficiency_string)
    if len(character.armor_proficiencies) > 0:
        armor_proficiency_string = "Armor proficiencies: " + list_to_str(character.armor_proficiencies)
        print(armor_proficiency_string)
    if len(character.weapon_proficiencies) > 0:
        weapon_proficiency_string = "Weapon proficiencies: " + list_to_str(character.weapon_proficiencies)
        print(weapon_proficiency_string)
    print(character.race.racial_traits_to_string())
    if len(character.cantrips) > 0:
        print("Known Cantrips: ")
        known_cantrips = "\t" + list_to_str(character.cantrips)
        print(known_cantrips)
    if len(character.spells) > 0:
        print("Known Spells: ")
        known_spells = "\t" + list_to_str(character.spells)
        print(known_spells)

    print("Class Features: ")
    print(character.dnd_class.class_features_to_string())

    print("Personality traits: " + list_to_str(character.personality_traits))
    print("Bonds: " + list_to_str(character.bonds))
    print("Flaws: " + list_to_str(character.flaws))
    print("Ideals: " + list_to_str(character.ideals))


def dnd_character_creation():
    insert_dnd5_background()
    insert_dnd5_language()
    insert_dnd5_race()
    insert_dnd5_classes()
    # getting all lists for backgrounds, races, languages and classes
    # todo: make lists for every db data
    background_name_list = get_all_background_names()
    race_name_list = get_all_races_names()
    language_list = get_all_languages()
    classes_list = get_all_classes_names()
    unrestricted_language_list = get_all_unrestricted_languages()

    # Name choice
    print("Choose character name")
    character_name = input()

    # Stat generations
    choosing_attributes = True
    while choosing_attributes:
        print("How do you want the stats to be generated ?\n" + dict_to_str(GENERATION_TYPES))
        generation = input()
        attributes = []
        if int(generation) == 4:
            print("Please input the 6 stats you want to use in order, for Strength, Dexterity, Constitution, "
                  "Intelligence, Wisdom, and Charisma")
            while len(attributes) < 6:
                att = input()
                int_att = int(att)
                if int_att < 5 or int_att > 20:
                    print("Your attributes should not go lower than 5 or higher than 20")
                else:
                    attributes.append(int_att)
        dnd_character = Dnd5Character(character_name.strip(), int(generation), stats=attributes)
        print("Your attributes are: " + dnd_character.attributes_to_str())
        print("If you accept these attributes, enter yes")
        acceptance = input().strip()
        if acceptance == "yes":
            choosing_attributes = False

    # Race choice
    choice_not_validated = True
    while choice_not_validated:
        print("Choose your race:\n" + list_to_str(race_name_list))
        race_choice = input().strip()
        if is_valid_choice(race_name_list, race_choice):
            race = look_for_race_by_name(race_choice)
            print("This is what this race would give you:")
            print(race.to_cli_string())
            print("Do you confirm this choice?")
            confirm = input().strip()
            if confirm == "yes":
                dnd_character.set_race(race)
                print("You have chosen the race: " + race.name)
                choice_not_validated = False

    # Racial trait choices
    racial_traits_choices_nb, racial_traits_choices_list = race.get_racial_traits()
    if racial_traits_choices_nb > 0:
        print("This race offers traits to choose from: ")
        for i in range(racial_traits_choices_nb):
            print(racial_traits_choices_list[i]["name"])

    # Racial tool choices
    tool_choices_nb, tool_choices = race.get_racial_tools()
    if tool_choices_nb > 0:
        print("Your race offers tool proficiency choices: pick "
              + str(tool_choices_nb) + " choices among the following list: ")
        print(list_to_str(tool_choices))
        tool_choice = input().strip()
        for i in range(tool_choices_nb):
            while not is_valid_choice(tool_choices, tool_choice):
                print("Choose a tool kit that is in the list above")
                tool_choice = input().strip()
            dnd_character.tool_proficiencies.add(tool_choice)

    # Racial cantrip choices
    cantrip_choice_nb, cantrip_choice_list = race.get_racial_cantrips()
    if cantrip_choice_nb > 0:
        print("Your race offers cantrip choices: pick " + str(cantrip_choice_nb) + " choices among the following list: ")
        print(list_to_str(cantrip_choice_list))
        cantrip_choice = input().strip()
        for i in range(cantrip_choice_nb):
            while not is_valid_choice(cantrip_choice_list, cantrip_choice):
                print("Choose a cantrip that is in the list above")
                cantrip_choice = input().strip()
            dnd_character.add_cantrip(cantrip_choice)

    # Skill choice from race possibilities
    skill_choice_number, skill_choice_options = race.get_racial_skills_choices()
    if skill_choice_number > 0:
        print("You have bonus proficiencies, pick " + str(skill_choice_number)
              + " among the following:\n" + list_to_str(skill_choice_options))
        proficiency_choices = []
        for i in range(skill_choice_number):
            prof_choice = input().strip()
            if is_valid_choice(skill_choice_options, prof_choice):
                proficiency_choices.append(prof_choice)
        dnd_character.set_bonus_skill_proficiencies(proficiency_choices)

    # Language choice from race possibilities
    if dnd_character.race.bonus_languages > 0:
        print("You have bonus languages, pick " + str(dnd_character.race.bonus_languages)
              + " among the following:\n" + list_to_str(unrestricted_language_list))
        language_choices = []
        for i in range(race.bonus_languages):
            lang_choice = input().strip()
            if is_valid_choice(unrestricted_language_list, lang_choice):
                language_choices.append(lang_choice)
        dnd_character.set_bonus_languages(language_choices)

    # Age choice
    print("Pick your age, " + race.name +
          " are usually between " + race.age_bracket[0] + " and " + race.age_bracket[1]
          + " years old.")
    age_choice = input()
    dnd_character.set_age(age_choice)

    # Alignment choice
    print("Choose your alignment:\n LG for Lawful Good, NG for Neutral Good, CG for Chaotic Good\n"
          + " LN for Lawful Neutral, TN for True Neutral, CN for Chaotic Neutral\n LE for Lawful Evil"
          + ", NE for Neutral Evil, CE for Chaotic Evil")
    alignment_choice = input()
    dnd_character.set_alignment(alignment_choice.strip())

    #  Background choice
    print("Choose your background:\n" + list_to_str(background_name_list))
    background_choice = input().strip()
    background_accepted = False
    while not background_accepted:
        while not is_valid_choice(background_name_list, background_choice):
            background_choice = input().strip()
        background = get_background_by_name(background_choice)
        print("Description: " + background.description)
        print("Background Feature: " + background.feature_description)
        print("Do you accept this background?")
        accept = input().strip()
        if accept == 'yes':
            background_accepted = True
    dnd_character.set_background(background)
    if background.feature_choice is not '':
        print("Your background has the following feature: " + background.feature_choice +
              "you can choose from the following table: ")
        print(list_to_str_with_number_and_line(background.feature_choice_table))
    if background.bonus_languages > 0:
        print("You have " + str(background.bonus_languages) + " bonus languages to pick: ")
        print(list_to_str(language_list))
        while background.bonus_languages > 0:
            language_choices = []
            language_input = input().strip()
            if is_valid_choice(unrestricted_language_list, language_input):
                language_choices.append(language_input)
                background.bonus_languages -= 1
            dnd_character.set_bonus_languages(language_choices)
    # choose personality trait
    print("You may choose one of these personality traits or type your own: ")
    print(list_to_str_with_number_and_line(background.personality_traits))
    personality_choice = input().strip()
    if int(personality_choice) < len(background.personality_traits):
        dnd_character.personality_traits.append(background.personality_traits[int(personality_choice)-1])
    else:
        dnd_character.personality_traits.append(personality_choice)
    print("You may choose a second personality trait")
    personality_choice = input().strip()
    if int(personality_choice) < len(background.personality_traits):
        dnd_character.personality_traits.append(background.personality_traits[int(personality_choice)-1])
    else:
        dnd_character.personality_traits.append(personality_choice)
    # choose ideal
    print("You may choose one of these ideals or type your own: ")
    print(list_to_str_with_number_and_line(background.ideals))
    ideal_choice = input().strip()
    if int(ideal_choice) < len(background.ideals):
        dnd_character.ideals.append(background.ideals[int(ideal_choice)-1])
    else:
        dnd_character.ideals.append(ideal_choice)
    # choose bond
    print("You may choose one of these bonds or type your own: ")
    print(list_to_str_with_number_and_line(background.bonds))
    bond_choice = input().strip()
    if int(bond_choice) < len(background.bonds):
        dnd_character.bonds.append(background.bonds[int(bond_choice)-1])
    else:
        dnd_character.ideals.append(bond_choice)
    # choose flaw
    print("You may choose one of these flaws or type your own: ")
    print(list_to_str_with_number_and_line(background.flaws))
    flaw_choice = input().strip()
    if int(flaw_choice) < len(background.flaws):
        dnd_character.flaws.append(background.flaws[int(flaw_choice)-1])
    else:
        dnd_character.flaws.append(flaw_choice)

    # Class choice
    choice_not_validated = True
    while choice_not_validated:
        print("Choose your class:\n" + list_to_str(classes_list))
        class_choice = input().strip()
        if is_valid_choice(classes_list, class_choice):
            dnd_class = look_for_class_by_name(class_choice)
            print("This is what this class would give you:")
            print(dnd_class.to_cli_string())
            print("Do you confirm this choice?")
            confirm = input().strip()
            if confirm == "yes":
                dnd_character.set_class(dnd_class)
                print("You have chosen the class: " + dnd_class.name)
                choice_not_validated = False

    # Cantrip and spells choice from class
    # Cantrip
    class_cantrip_choice_nb = dnd_character.dnd_class.cantrips_choice["number"]
    class_cantrip_choice = dnd_character.dnd_class.cantrips_choice["cantrips"]
    if class_cantrip_choice_nb > 0:
        print("You can choose " + str(
            class_cantrip_choice_nb) + " cantrip(s) from the following list:\n" + list_to_str(
            class_cantrip_choice))
        for i in range(class_cantrip_choice_nb):
            choice = input().strip()
            dnd_character.add_cantrip(choice)
    # Spell lvl 1
    class_spell_choice_nb = dnd_character.dnd_class.level_one_choice["number"]
    class_spell_choice = dnd_character.dnd_class.level_one_choice["spells"]
    if class_cantrip_choice_nb > 0:
        print("You can choose " + str(
            class_spell_choice_nb) + " spell(s) from the following list:\n" + list_to_str(
            class_spell_choice))
        for i in range(class_spell_choice_nb):
            choice = input().strip()
            dnd_character.add_spell(choice, class_spell_choice)

    # Skill choice from class possibilities
    skill_choices = dnd_character.dnd_class.skill_proficiency_choices["number"]
    skill_options = dnd_character.dnd_class.skill_proficiency_choices["skill_proficiencies"]
    if skill_choices > 0:
        print("You already have these proficiencies: " + list_to_str(dnd_character.skill_proficiencies))
        print("You have bonus proficiencies, pick " + str(skill_choices)
              + " among the following:\n" + list_to_str(skill_options))
        proficiency_choices = set([])
        chosen_skills = skill_choices
        while chosen_skills > 0:
            print("You have " + str(chosen_skills) + " skills left to pick.")
            prof_choice = input().strip()
            for j in dnd_character.skill_proficiencies:
                if prof_choice == j:
                    print("You already have this skill, choose another")
                    prof_choice = input().strip()
            # if the skill has been added to the chosen list we ask for another choice
            if is_valid_choice(proficiency_choices, prof_choice):
                print("You already picked this skill, choose another")
                prof_choice = input().strip()
            if is_valid_choice(skill_options, prof_choice):
                proficiency_choices.add(prof_choice)
                chosen_skills -= 1
        dnd_character.set_bonus_skill_proficiencies(proficiency_choices)

    # Adding Tools proficiencies from class
    tool_choices = dnd_character.dnd_class.tool_proficiency_choices["number"]
    tools_options = dnd_character.dnd_class.tool_proficiency_choices["tool_proficiencies"]
    if tool_choices > 0 and tool_choices != len(tools_options):
        if len(dnd_character.tool_proficiencies) > 0:
            print("You already have these tool proficiencies: " + list_to_str(dnd_character.tool_proficiencies))
        print("You can choose " + str(tool_choices) + " tool proficiencies among the following:\n"
              + tools_options)
        tool_prof_choices = []
        for i in range(tool_choices):
            prof_choice = input()
            if is_valid_choice(tools_options, prof_choice):
                tool_prof_choices.append(prof_choice)
        dnd_character.set_bonus_tool_proficiencies(tool_prof_choices)
    elif tool_choices > 0:
        dnd_character.set_bonus_tool_proficiencies(tools_options)
        print("You gain the following tool proficiencies: " + list_to_str(tools_options))

    # Check for choices of class feature
    features = dnd_character.dnd_class.feature_choices
    if len(features) > 0:
        for i in range(len(features)):
            print("You get the following feature: " + features[i]["name"])
            print(features[i]["description"])
            choices = features[i]["choice_table"]
            if isinstance(choices, dict):
                for j in choices:
                    print("\t" + j + ": " + features[i]["choice_table"][j])
            else:
                for j in choices:
                    print("\t" + j)
            choice = input()
            dnd_character.dnd_class.choose_feature(features[i]["name"], choice)

    # Calculate HP at the end
    dnd_character.calc_hp_first_lvl()

    # Display character
    cli_display(dnd_character)

    # Save character to a json format
    print("Do you want to save your character?")
    answer = input().strip()
    if answer == "yes":
        dnd_character.export_json()
