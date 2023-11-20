from source.database.database_access import create_connection
from source.multimedia_library.images import get_image
from source.pan_zoom_sprites.pan_zoom_planet_classes.pan_zoom_planet import PanZoomPlanet
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_handler import pan_zoom_handler
from source.pan_zoom_sprites.pan_zoom_sprite_base.pan_zoom_sprite_handler import sprite_groups
from source.utils import global_params
from source.utils.colors import colors


class PlanetFactory:
    def save_planets(self):
        # save_load each file
        for planet in sprite_groups.planets:
            planet.save_to_db()

    def load_planets(self):
        # save_load each file
        for planet in sprite_groups.planets:
            planet.update()
            planet.load_from_db()

    def delete_planets(self):
        for planet in sprite_groups.planets:
            sprite_groups.planets.remove(planet)
            planet.__delete__()
            planet.kill()

    def create_planets_from_db(self, database_file):
        """loads values from database and construct the planet object
        """
        conn = create_connection(database_file)
        cur = conn.cursor()
        ids_tuples_list = cur.execute("select id from planets").fetchall()
        ids = [t[0] for t in ids_tuples_list]

        for id in ids:
            self.create_planet(cur, id)

        self.load_planets()

    def create_planet(self, cur, id):
        image_name = cur.execute(f"select image_name_small from planets where id = {id}").fetchone()[0]
        width, height = map(int, image_name.split("_")[1].split(".")[0].split("x"))
        type = cur.execute(f"select type from planets where id = {id}").fetchone()[0]

        gif = None

        has_atmosphere = cur.execute(f"SELECT has_atmosphere FROM planets WHERE id = {id}").fetchone()[0]
        if type == "sun":
            gif = "sun.gif"

        if type == "moon":
            gif = "moon1.gif"

        elif has_atmosphere:
            gif = "atmosphere.gif"

        pan_zoom_planet_button = PanZoomPlanet(
            win=global_params.win,
            x=cur.execute(f"select world_x from planets where id = {id}").fetchone()[0],
            y=cur.execute(f"select world_y from planets where id = {id}").fetchone()[0],
            width=int(cur.execute(f"select world_width from planets where id = {id}").fetchone()[0]),
            height=int(cur.execute(f"select world_height from planets where id = {id}").fetchone()[0]),
            pan_zoom=pan_zoom_handler,
            isSubWidget=False,
            image=get_image(
                cur.execute(f"select image_name_small from planets where id = {id}").fetchone()[0]),
            image_name=cur.execute(f"select image_name_small from planets where id = {id}").fetchone()[0],
            transparent=True,
            info_text=cur.execute(f"select info_text from planets where id = {id}").fetchone()[0],
            text=cur.execute(f"select name from planets where id = {id}").fetchone()[0],
            textColour=colors.frame_color,
            property="planet",
            name=cur.execute(f"select name from planets where id = {id}").fetchone()[0],
            parent=global_params.app,
            tooltip="send your ship to explore the planet!",
            possible_resources=eval(
                cur.execute(f"select possible_resources from planets where id = {id}").fetchone()[0]),
            moveable=global_params.moveable,
            hover_image=get_image("selection_150x150.png"),
            has_atmosphere=cur.execute(f"SELECT has_atmosphere FROM planets WHERE id = {id}").fetchone()[0],
            textVAlign="below_the_bottom",
            layer=0,
            id=id,
            orbit_object_id=cur.execute(f"select orbit_object_id from planets where id = {id}").fetchone()[0],
            image_name_small=cur.execute(f"select image_name_small from planets where id = {id}").fetchone()[0],
            image_name_big=cur.execute(f"select image_name_big from planets where id = {id}").fetchone()[0],
            buildings_max=cur.execute(f"select buildings_max from planets where id = {id}").fetchone()[0],
            orbit_speed=cur.execute(f"select orbit_speed from planets where id = {id}").fetchone()[0],
            orbit_angle=cur.execute(f"select orbit_angle from planets where id = {id}").fetchone()[0],
            building_slot_amount=
            cur.execute(f"select building_slot_amount from planets where id = {id}").fetchone()[0],
            alien_population=cur.execute(f"select alien_population from planets where id = {id}").fetchone()[0],
            specials=cur.execute(f"select specials from planets where id = {id}").fetchone()[0],
            type=type,
            gif=gif,
            debug=False,
            align_image="center"
            )
        # pan_zoom_planet_button.load_from_db()
        sprite_groups.planets.add(pan_zoom_planet_button)
        # pan_zoom_planet_button.load_from_db()

planet_factory = PlanetFactory()