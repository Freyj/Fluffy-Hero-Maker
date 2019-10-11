from databases.dnd5_backgrounds import insert_dnd5_background
from databases.dnd5_classes_db import insert_dnd5_classes
from databases.dnd5_db import drop_all_tables, create_dnd5_db
from databases.dnd5_languages_db import insert_dnd5_language
from databases.dnd5_monster_db import insert_dnd5_monster_data
from databases.dnd5_races_db import insert_dnd5_race
from databases.dnd5_spell_db import insert_dnd5_spell_data


def create_database():
    create_dnd5_db()


def initialize_all_data():
    insert_dnd5_spell_data()
    insert_dnd5_background()
    insert_dnd5_language()
    insert_dnd5_race()
    insert_dnd5_classes()
    insert_dnd5_monster_data()


def delete_all_data():
    drop_all_tables()
