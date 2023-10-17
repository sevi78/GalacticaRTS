from source.configuration.config import production, prices, ship_prices, planetary_defence_prices
from source.database.database_access import get_dict_from_database
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups


def create_info_panel_planet_text(self):
    db_dict = get_dict_from_database(self.id)
    text_keys = ["name", "possible_resources", "specials", "buildings_max", "alien_population", "orbit_speed",
                 "orbit_distance", "type"]
    orbit_object = [i for i in sprite_groups.planets if i.id == self.orbit_object_id]

    info = {}
    for key, value in db_dict.items():
        if key in text_keys:
            if "[" in str(value):
                value = eval(value)
            info[key] = value

    name = info['name']
    alien_population = info['alien_population']
    buildings_max = info['buildings_max']
    specials = info['specials']
    possible_resources = info['possible_resources']
    orbit_speed = info['orbit_speed']
    orbit_distance = str(round(info['orbit_distance'] / 1000, 1)) + " million kilometers"
    type = info['type']

    text = f"Welcome to {name}!\n\n"
    if alien_population == 0:
        text += f"You are the first to arrive on this {type}. It's a blank slate waiting for you to make your mark.\n"
    else:
        text += f"You are not alone on this {type}. There are {alien_population} aliens living here already.\n"

    text += f"You can build up to {buildings_max} buildings on this planet.\n"
    if specials:
        text += f"There are special buildings available: {specials}.\n"
    else:
        text += "There are no special buildings available on this planet.\n"

    text += "Possible resources on this planet include:\n\n"
    for resource in possible_resources:
        text += f"- {resource}\n"

    text += f"\nThe planet's orbits around its sun at a distance of {orbit_distance} with a speed of {orbit_speed}.\n"

    return text


def create_info_panel_building_text():
    building_panel_info_text = {}
    text = ""
    for building, dict in prices.items():
        text = building + ":" + "\n"
        text += "\n" + "prices:" + "\n\n"

        for resource, value in dict.items():
            text += resource + ": " + str(value) + "\n"
        text += "\n" + "production: " + "\n"
        text += "\n"

        for r, v in production[building].items():
            text += r + ": " + str(v) + "\n"

        building_panel_info_text[building] = text

    return building_panel_info_text


def create_info_panel_ship_text(ship):
    text = ""
    text = ship + ":" + "\n"
    text += "\n" + "prices:" + "\n\n"

    for ship_name, dict in ship_prices.items():
        if ship_name == ship:
            for resource, value in dict.items():
                text += resource + ": " + str(value) + "\n"

    return text


def create_info_panel_planetary_defence_text(item):
    text = ""
    text = item + ":" + "\n"
    text += "\n" + "prices:" + "\n\n"

    for item_name, dict in planetary_defence_prices.items():
        if item_name == item:
            for resource, value in dict.items():
                text += resource + ": " + str(value) + "\n"

    return text
