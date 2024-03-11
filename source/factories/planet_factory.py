import copy
import random
import string

from source.configuration.game_config import config
from source.handlers.color_handler import colors
from source.handlers.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.multimedia_library.images import get_image
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet import PanZoomPlanet
from source.text.text_formatter import to_roman


class PlanetFactory:
    def delete_planets(self):
        for planet in sprite_groups.planets:
            sprite_groups.planets.remove(planet)
            planet.__delete__()
            planet.kill()
        config.app.selected_planet = None

    def create_planets_from_data(self, data, **kwargs):
        # pprint.pprint(data)

        for key, value in data["celestial_objects"].items():
            if "explored" in data["celestial_objects"][key].keys():
                explored = kwargs.get("explored", data["celestial_objects"][key]["explored"])
            else:
                explored = False

            if "buildings" in value.keys():
                buildings = data["celestial_objects"][key]["buildings"]
            else:
                buildings = []

            if type(value) == list:
                value = eval(value)

            pan_zoom_planet_button = PanZoomPlanet(
                win=config.win,
                x=value["world_x"],
                y=value["world_y"],
                width=int(value["world_width"]),
                height=int(value["world_height"]),
                pan_zoom=pan_zoom_handler,
                isSubWidget=False,
                image=get_image(value["image_name_small"]),
                image_name=value["image_name_small"],
                transparent=True,
                info_text=value["info_text"],
                text=value["name"],
                textColour=colors.frame_color,
                property="planet",
                name=value["name"],
                parent=config.app,
                tooltip="send your ship to explore the planet!",
                possible_resources=value["possible_resources"],
                moveable=config.moveable,
                hover_image=get_image("selection_150x150.png"),
                textVAlign="below_the_bottom",
                layer=4,
                id=value["id"],
                orbit_object_id=value["orbit_object_id"],
                image_name_small=value["image_name_small"],
                image_name_big=value["image_name_big"],
                buildings_max=value["buildings_max"],
                buildings=buildings,  # value["buildings"],
                orbit_speed=value["orbit_speed"],
                orbit_angle=value["orbit_angle"],
                building_slot_amount=value["building_slot_amount"],
                alien_population=value["alien_population"],
                specials=value["specials"],
                type=value["type"],
                gif=value["atmosphere_name"],
                debug=False,
                align_image="center",
                atmosphere_name=value["atmosphere_name"],
                data=data["celestial_objects"][key]
                )

            if explored:
                pan_zoom_planet_button.get_explored(-1)

            # update stats
            pan_zoom_planet_button.set_population_limit()

            # register
            sprite_groups.planets.add(pan_zoom_planet_button)

    def get_all_planets(self, keys:list):
        """
        returns a list of all planets in the game with the same type as in list
        :param keys: list of planet types
        """
        return [_ for _ in sprite_groups.planets.sprites() if _.type in keys]

    def get_all_planet_names(self):
        return [i.name for i in sprite_groups.planets.sprites()]

    def generate_planet_names(self):
        solar_system_names = copy.deepcopy(config.app.level_handler.level_dict_generator.solar_system_names)
        suns = [i for i in sprite_groups.planets if i.type == "sun"]

        for sun in suns:
            sun.name = solar_system_names.pop(solar_system_names.index(random.choice(solar_system_names)))
            planets = sorted([i for i in sprite_groups.planets if
                              i.type == "planet" and i.orbit_object_id == sun.id], key=lambda
                planet: planet.orbit_distance)
            for index, planet in enumerate(reversed(planets)):
                planet.name = f"{sun.name} {to_roman(len(planets) - index)}"
                moons = sorted([i for i in sprite_groups.planets if
                                i.type == "moon" and i.orbit_object_id == planet.id], key=lambda
                    moon: moon.orbit_distance)
                for index_, moon in enumerate(reversed(moons)):
                    moon.name = f"{planet.name} - {string.ascii_uppercase[len(moons) - 1 - index_]}"

        for i in sprite_groups.planets.sprites():
            i.string = i.name

    def explore_planets(self):
        for i in sprite_groups.planets.sprites():
            if not i.explored:
                i.get_explored(-1)
            else:
                i.explored = False
                i.string = "?"
                i.just_explored = False

    def delete_planet(self, selected_planet):
        if selected_planet:
            sprite_groups.planets.remove(selected_planet)
            selected_planet.__delete__()
            selected_planet.kill()

            # delete gif handlers attached to planet
            for i in sprite_groups.gif_handlers.sprites():
                if i.parent == selected_planet:
                    i.end_object()


planet_factory = PlanetFactory()
