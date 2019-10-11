# Fluffy Hero Maker
[![Build Status](https://travis-ci.org/Freyj/Fluffy-Hero-Maker.svg?branch=master)](https://travis-ci.org/Freyj/Fluffy-Hero-Maker)
## What is this?
This is an attempt at having a semi-automatic way of building characters or accessing some of my data for my tabletop rpg games.

## What games does it cover?
For now, only Dungeons and Dragons 5th Edition (SRD), but I plan to cover other systems too, later on.

## How do I add data?
It uses json files to fill its databases, and the only files on this are from data that is part of the SRD  (https://dnd.wizards.com/articles/features/systems-reference-document-srd)
To add data, you can find templates of the json structures in the **utils** directory, and the data needs to be added in the **databases/data/** proper directory depending on if you want to add races, spells, monsters, classes, or backgrounds.

## How do I run it?
- You need python 3.7 installed on your machine.
- Ideally, just launching ```python3 cli_main.py -debug``` should do the trick.
*This is only in command-line interface for now, graphical interfaces are a pest.*
- *[also, this has only been tested on a linux machine with an Ubuntu distribution, so no guarantees]*

The -debug option is required to have the database for now, at least on the first launch. If you make any addition in 
json files or want to update the database, you need to leave the -debug option on.

## What can I do with it?
You can create a character, picking a name, race, class, and background. 
You can display monster stats or spell stats also.

## What is lacking?
A lot (just look at the issues).
* All the SRD data taken into account.
* Cleaner code.
* Cleaner everything.
* Not CLI display
* Enough automated tests.

## Why this name?
Because this world needs more fluffy things. Also it is a partially wrong name, as it is more of a fluffy-helper than a fluffy-hero-maker, but eh.

## Danger zone
* High risk of things changing a lot because this is very flimsy.
* Also, high probability of bugs
* Also, I sometimes forget to use the python things, and reinvent the wheel for no reason

## Licensing
Not exactly sure yet how I license this, so for now, it's ALL MINE and you're allowed to look at it and be amazed (or shocked).
(keeping this as a note for later : https://www.gnu.org/licenses/gpl-howto.html).
(Of course, the SRD is not mine.)

## Can I help?
Check the [CONTRIBUTING.md](https://github.com/Freyj/Fluffy-Hero-Maker/blob/master/CONTRIBUTING.md) to see more about how to contribute.