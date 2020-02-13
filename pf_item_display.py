from databases.pf.pf_item_db import look_for_item_by_name, get_all_items_names_from_db


def pf_item_display():
    print("For a specific item, type 1, 2 to get all item names in the database")
    choice = input()
    if choice == "1":
        print("Please give the name of the item you are looking for:")
        item_name = input().strip()
        item = look_for_item_by_name(item_name)
        if item is None:
            print("No spell found with name: {item}".format(item=item_name))
        else:
            print(item.cli_display_string())
