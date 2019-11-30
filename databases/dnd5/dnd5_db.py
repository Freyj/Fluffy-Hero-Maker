import sqlite3

from databases.dnd5.dnd5_backgrounds import CREATE_BACKGROUND_TABLE_REQUEST, DROP_BACKGROUND_TABLE_REQUEST
from databases.dnd5.dnd5_classes_db import CREATE_CLASS_TABLE_REQUEST, DROP_CLASS_TABLE_REQUEST
from databases.dnd5.dnd5_races_db import CREATE_RACE_TABLE_REQUEST, DROP_RACE_TABLE_REQUEST
from databases.dnd5.dnd5_languages_db import CREATE_LANGUAGE_TABLE_REQUEST, DROP_LANGUAGE_TABLE_REQUEST
from databases.dnd5.dnd5_monster_db import CREATE_MONSTER_TABLE_REQUEST, DROP_MONSTER_TABLE_REQUEST
from databases.dnd5.dnd5_spell_db import CREATE_SPELL_TABLE_REQUEST, DROP_SPELL_TABLE_REQUEST


def drop_all_tables():
    """"
    Drops all tables (mostly for testing purposes and dev)
    """
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    # Drop the spells table
    cursor.execute(DROP_SPELL_TABLE_REQUEST)
    connection.commit()
    cursor = connection.cursor()
    # Drop the monsters table
    cursor.execute(DROP_MONSTER_TABLE_REQUEST)
    connection.commit()
    cursor = connection.cursor()
    # Drop the backgrounds table
    cursor.execute(DROP_BACKGROUND_TABLE_REQUEST)
    connection.commit()
    cursor = connection.cursor()
    # Drop the languages table
    cursor.execute(DROP_LANGUAGE_TABLE_REQUEST)
    connection.commit()
    # Drop the races table
    cursor.execute(DROP_RACE_TABLE_REQUEST)
    connection.commit()
    # Drop the classes table
    cursor.execute(DROP_CLASS_TABLE_REQUEST)
    connection.commit()
    connection.close()


def create_dnd5_db():
    """"
    Creates the database for dnd5 data if it does not already exist
    :returns nothing
    """
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    # create the spells table
    cursor.execute(CREATE_SPELL_TABLE_REQUEST)
    connection.commit()
    # create the monsters table
    cursor.execute(CREATE_MONSTER_TABLE_REQUEST)
    connection.commit()
    # create the backgrounds table
    cursor.execute(CREATE_BACKGROUND_TABLE_REQUEST)
    connection.commit()
    # create the languages table
    cursor.execute(CREATE_LANGUAGE_TABLE_REQUEST)
    connection.commit()
    # create the races table
    cursor.execute(CREATE_RACE_TABLE_REQUEST)
    connection.commit()
    # create the classes table
    cursor.execute(CREATE_CLASS_TABLE_REQUEST)
    connection.commit()
    connection.close()


