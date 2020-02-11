from flask import Flask, render_template

from characters.DnD5Character import generate_random_dnd_character
from databases.dnd5.dnd5_monster_db import get_random_monster, get_all_monsters_names_from_db, get_monster_by_name
from databases.dnd5.dnd5_spell_db import get_random_spell, get_all_spell_names_from_db, look_for_spell_by_name


app = Flask(__name__, template_folder="../utils/jinja_templates")


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/random-dnd-spell")
def random_spell():
    spell = get_random_spell()
    return render_template('dndSpell.html', spell=spell)


@app.route("/random-dnd-monster")
def random_monster():
    monster = get_random_monster()
    return render_template('dndMonster.html', monster=monster)


@app.route("/all-dnd-monsters")
def get_all_monsters():
    monsterList = get_all_monsters_names_from_db()
    return render_template('dndAllMonstersList.html', list=monsterList)


@app.route("/all-dnd-spells")
def get_all_spells():
    spellList = get_all_spell_names_from_db()
    return render_template('dndAllSpellsList.html', list=spellList)


@app.route("/dnd-spell/<name>")
def get_spell(name=None):
    spell = look_for_spell_by_name(name)
    return render_template('dndSpell.html', spell=spell)


@app.route("/dnd-monster/<name>")
def get_monster(name=None):
    spell = get_monster_by_name(name)
    return render_template('dndMonster.html', monster=spell)


@app.route("/dnd-random-character-gen/<name>")
def random_dnd_character(name=None):
    character = generate_random_dnd_character(name)
    return render_template('dndCharacter.html', character=character)


@app.route("/classic-traveller-character-gen")
def classic_traveller_rand_char():
    character = random_classic_traveller_character()
    return render_template('CTCharacter.html', character=character)