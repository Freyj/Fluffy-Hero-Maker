import requests
import time


def get_monsters_from_api():
    r = requests.get('https://api.open5e.com/monsters/')
    print("A request")
    json_data = r.json()
    # get the info whether there is more results to get (and the URI)
    next_result = json_data["next"]
    page_monsters = json_data["results"]
    result_monsters = [format_monsters_from_json(page_monsters)]
    while next_result is not None:
        # let's not spam the API
        time.sleep(1)
        r = requests.get(next_result)
        print("A request")
        json_data = r.json()
        next_result = json_data["next"]
        page_monsters = json_data["results"]
        result_monsters.extend(format_monsters_from_json(page_monsters))

    print(result_monsters)


def get_monsters_from_api_by_type(type: str):
    uri = 'https://api.open5e.com/monsters/?type=' + type
    r = requests.get(uri)
    print("A request")
    json_data = r.json()
    # get the info whether there is more results to get (and the URI)
    next_result = json_data["next"]
    page_monsters = json_data["results"]
    result_monsters = [format_monsters_from_json(page_monsters)]
    while next_result is not None:
        # let's not spam the API
        time.sleep(1)
        r = requests.get(next_result)
        print("A request")
        json_data = r.json()
        next_result = json_data["next"]
        page_monsters = json_data["results"]
        result_monsters.extend(format_monsters_from_json(page_monsters))

    print(result_monsters[0])
    print(len(result_monsters))


def format_monsters_from_json(json_data):
    monsters = []
    for monster in json_data:
        walking_speed = monster['speed']['walk'] if 'walk' in monster['speed'] else 0
        climbing_speed = monster['speed']['climb'] if 'climb' in monster['speed'] else 0
        burrowing_speed = monster['speed']['burrow'] if 'burrow' in monster['speed'] else 0
        swimming_speed = monster['speed']['swim'] if 'swim' in monster['speed'] else 0
        flying_speed = monster['speed']['fly'] if 'fly' in monster['speed']else 0
        item = {
            "name": monster["name"],
            "size": monster["size"],
            "type": monster["type"],
            "subtype": monster["subtype"],
            "alignment": monster["alignment"],
            "armor_class": monster["armor_class"],
            "armor_desc": monster["armor_desc"],
            "hit_points": monster["hit_points"],
            "hit_dice": monster["hit_dice"],
            "flying_speed": flying_speed,
            "climbing_speed": climbing_speed,
            "walking_speed": walking_speed,
            "burrowing_speed": burrowing_speed,
            "swimming_speed": swimming_speed,
            "strength": monster["strength"],
            "dexterity": monster["dexterity"],
            "constitution": monster["constitution"],
            "intelligence": monster["intelligence"],
            "wisdom": monster["wisdom"],
            "charisma": monster["charisma"],
            "strength_save": monster["strength_save"],
            "dexterity_save": monster["dexterity_save"],
            "constitution_save": monster["constitution_save"],
            "intelligence_save": monster["intelligence_save"],
            "wisdom_save": monster["wisdom_save"],
            "charisma_save": monster["charisma_save"]
        }
        monsters.append(item)

    return monsters


if __name__ == "__main__":
    # get_monsters_from_api_by_type("humanoid")
    get_monsters_from_api()