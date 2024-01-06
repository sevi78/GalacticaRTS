from source.multimedia_library.images import get_image
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet import PanZoomPlanet
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups
from source.configuration import global_params
from source.handlers.color_handler import colors


class PlanetFactory:
    def delete_planets(self):
        for planet in sprite_groups.planets:
            sprite_groups.planets.remove(planet)
            planet.__delete__()
            planet.kill()
        global_params.app.selected_planet = None
    def create_planets_from_data(self, data, **kwargs):
        explored = kwargs.get("explored", False)
        for key, value in data["celestial_objects"].items():
            pan_zoom_planet_button = PanZoomPlanet(
                win=global_params.win,
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
                parent=global_params.app,
                tooltip="send your ship to explore the planet!",
                possible_resources=value["possible_resources"],
                moveable=global_params.moveable,
                hover_image=get_image("selection_150x150.png"),
                textVAlign="below_the_bottom",
                layer=4,
                id=value["id"],
                orbit_object_id=value["orbit_object_id"],
                image_name_small=value["image_name_small"],
                image_name_big=value["image_name_big"],
                buildings_max=value["buildings_max"],
                orbit_speed=value["orbit_speed"],
                orbit_angle=value["orbit_angle"],
                building_slot_amount=value["building_slot_amount"],
                alien_population=value["alien_population"],
                specials=value["specials"],
                type=value["type"],
                gif=value["atmosphere_name"],
                debug=False,
                align_image="center",
                atmosphere_name=value["atmosphere_name"]
                )
            pan_zoom_planet_button.explored = explored
            sprite_groups.planets.add(pan_zoom_planet_button)

    def get_all_planets(self, keys):
        return [_ for _ in sprite_groups.planets.sprites() if _.type in keys]


planet_factory = PlanetFactory()
