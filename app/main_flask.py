from flask import Flask, render_template

from dnd5.DnD5Character import generate_random_dnd_character
from databases.dnd5.dnd5_monster_db import get_random_monster, get_all_monsters_names_from_db, get_monster_by_name
from databases.dnd5.dnd5_spell_db import get_random_spell, get_all_spell_names_from_db, look_for_spell_by_name
from traveller.gen_ct_char import random_classic_traveller_character, random_classic_traveller_party_generator
from traveller.gen_ct_system import random_ct_world_gen

app = Flask(__name__, template_folder="../utils/jinja_templates")


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/random-dnd-spell")
def random_spell():
    spell = get_random_spell()
    return render_template('dnd5/dndSpell.html', spell=spell)


@app.route("/random-dnd-monster")
def random_monster():
    monster = get_random_monster()
    return render_template('dnd5/dndMonster.html', monster=monster)


@app.route("/all-dnd-monsters")
def get_all_monsters():
    monsterList = get_all_monsters_names_from_db()
    return render_template('dnd5/dndAllMonstersList.html', list=monsterList)


@app.route("/all-dnd-spells")
def get_all_spells():
    spellList = get_all_spell_names_from_db()
    return render_template('dnd5/dndAllSpellsList.html', list=spellList)


@app.route("/dnd-spell/<name>")
def get_spell(name=None):
    spell = look_for_spell_by_name(name)
    return render_template('dnd5/dndSpell.html', spell=spell)


@app.route("/dnd-monster/<name>")
def get_monster(name=None):
    spell = get_monster_by_name(name)
    return render_template('dnd5/dndMonster.html', monster=spell)


@app.route("/dnd-random-character-gen/<name>")
@app.route("/dnd-random-character-gen/")
def random_dnd_character(name=None):
    character = generate_random_dnd_character(name)
    return render_template('dnd5/dndCharacter.html', character=character)


@app.route("/classic-traveller-character-gen/")
@app.route("/classic-traveller-character-gen/<name>")
@app.route("/classic-traveller-character-gen/<name>/<alive>")
def classic_traveller_rand_char(name=None, alive=None):
    if alive is not None:
        check_survival = True
    else:
        check_survival = False
    character = random_classic_traveller_character(name, must_be_alive=check_survival)
    jsonforchar = character.export_character_to_json()
    return render_template('classic_traveller/ctCharacter.html',
                           character=character,
                           upp=character.get_upp(),
                           rank=character.get_rank(),
                           noble_rank=character.get_noble_rank(),
                           json_char=jsonforchar)


@app.route("/classic-traveller-rand-party-gen")
def random_ct_party_gen():
    characters = random_classic_traveller_party_generator()
    for i in characters:
        i.upp = i.get_upp()
        i.rank_name = i.get_rank()
        i.noble_rank = i.get_noble_rank()
    return render_template('classic_traveller/ctParty.html',
                           characters=characters)


@app.route("/classic-traveller-rand-world-gen/<name>")
@app.route("/classic-traveller-rand-world-gen/")
def random_classic_traveller_world_gen(name=None):
    world = random_ct_world_gen(name=name)
    return render_template('classic_traveller/ctWorld.html', world=world)
