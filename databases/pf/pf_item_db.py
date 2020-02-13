import json
import os
import sqlite3

from pf_item.PFItem import PFItem
from utils.dice_roller import roll_die

ITEM_DATA_DIR = 'databases/data/pf/items/'


CREATE_ITEM_TABLE_REQUEST = '''CREATE TABLE IF NOT EXISTS pf_items 
                        (id integer primary key, name text not null, type text, sub_type text,
                         buy_price text, weight integer, description text, special text
                         )'''

# 1: name
# 2: type
# 3: subtype
# 4: buy_price
# 5: weight
# 6: description
# 7: special
INSERT_ITEMS_INTO_REQUEST = '''INSERT INTO pf_items
                            (name, type, sub_type, buy_price, weight, description, special) values 
                            (?,?,?,?,?,?,?)'''


DROP_ITEM_TABLE_REQUEST = '''DROP TABLE IF EXISTS pf_items'''


def get_number_of_items_in_db():
    """
        Returns the number of items in the pf_items table
        :return: integer representing the number of items in the database
    """
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()

    select_request = '''SELECT count() from pf_items'''
    cursor.execute(select_request)
    number_of_rows = cursor.fetchone()[0]
    connection.close()
    return number_of_rows


def insert_pf_items_data():
    """
        Parses all the json files in the pf/items folder
        and inserts all the items in the database
        :return: nothing
        TODO: exceptions instead of prints for errors
    """
    if get_number_of_items_in_db() == 0:
        items = get_all_items_from_json()
        if len(items) > 0:
            connection = sqlite3.connect('dnd5_db.db')
            connection.executemany(INSERT_ITEMS_INTO_REQUEST, items)
            connection.commit()
            connection.close()
    else:
        print("Items already in database")


def get_all_items_from_json():
    """
        Parses the items from json and creates tuples to fill the database from it
        :return: the items as a list of tuples
    """
    items = []
    for file in os.listdir(ITEM_DATA_DIR):
        file_path = ITEM_DATA_DIR + file
        if file_path.endswith(".json"):
            with open(file_path, encoding='utf-8') as fd:
                json_data = json.load(fd)
                for item in json_data:
                    element = (item["name"],
                               item["type"],
                               item["sub_type"],
                               item["buy_price"],
                               item["weight"],
                               item["description"],
                               item["special"]
                               )
                    items.append(element)
    return items


def get_all_items_names_from_db():
    """
        Returns all the item names from the database
        :return: a list of strings
    """
    names = []
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT name from pf_items'''
    cursor.execute(select_request)
    records = cursor.fetchall()
    for i in records:
        names.append(i[0])
    connection.close()
    return names


def get_random_item():
    """
        Returns a random item from the database
        :return: a PFItem
    """
    number = get_number_of_items_in_db()
    roll = roll_die(number - 1)
    item = get_item_by_id(roll)
    return item


def get_item_by_id(item_id):
    """
        Returns one item as a PFItem object from the corresponding id in the database
        :param item_id: int
        :return: a PFItem object
    """
    if item_id > 0:
        connection = sqlite3.connect('dnd5_db.db')
        cursor = connection.cursor()
        select_request = '''SELECT * from pf_items WHERE id = (?) '''
        cursor.execute(select_request, (item_id,))
        record = cursor.fetchone()
        item = change_record_into_item(record)
        connection.close()
        return item
    return None


def look_for_item_by_name(name):
    """
    Returns an item from its name
    :parameter name: a string representing the name of the item
    :return PFItem object with the data of the item
    """
    item = PFItem("test")
    if name != "":
        connection = sqlite3.connect('dnd5_db.db')
        cursor = connection.cursor()
        select_request = '''SELECT * from pf_items WHERE name = (?) '''
        cursor.execute(select_request, (name,))
        record = cursor.fetchone()
        item = change_record_into_item(record)
        connection.close()
        return item
    return None


def change_record_into_item(record):
    """"
    Turns a record into an item object
    :parameter record: the database record as a tuple representing a item
    :return PFItem object with the proper data
    """
    item = PFItem("temp")
    if record is not None:
        item.name = record[1]
        item.type = record[2]
        item.sub_type = record[3]
        item.buy_price = record[4]
        item.weight = record[5]
        item.description = record[6]
        item.special = record[7]
        return item
    return None
