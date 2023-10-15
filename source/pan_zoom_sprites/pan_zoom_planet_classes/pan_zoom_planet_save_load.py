import json

from source.database.database_access import create_connection, get_database_file_path, select, insert, \
    get_dict_from_database


class PanZoomPlanetSaveLoad:
    def __init__(self):
        pass
    def save_to_db(self):
        # self.orbit_object_id = 5
        conn = create_connection(get_database_file_path())

        select_sql = f"SELECT * FROM planets WHERE id = '{self.id}'"
        existing_row = select(conn, select_sql)

        if len(existing_row) == 0:
            # Insert the planet into the database if it does not exist
            sql = (f"""
                INSERT INTO planets (id, level, name, world_x, world_y, world_width, world_height, info_text, population_grow, alien_population, buildings_max,
                building_slot_amount, specials, type, possible_resources, image_name_small, image_name_big, orbit_speed,
                orbit_object_id, orbit_distance, atmosphere_name, has_atmosphere, orbit_angle )

                VALUES(
                '{self.id}',
                '{self.level}',
                '{self.name}',
                '{self.world_x}',
                '{self.world_y}',
                '{self.world_width}',
                '{self.world_height}',
                '{self.info_text_raw}',
                '{self.population_grow}',
                '{self.alien_population}',
                '{self.buildings_max}',
                '{self.building_slot_amount}',
                '{self.specials}',
                '{self.type}',
                '{json.dumps(self.possible_resources)}',
                '{self.image_name_small}',
                '{self.image_name_big}',
                '{self.orbit_speed}',
                '{self.orbit_object_id}',
                '{self.orbit_distance}',
                '{self.atmosphere_name}',
                '{self.has_atmosphere}',
                '{self.orbit_angle}'
                );
                """)
            insert(conn, sql)
            print(f"Planet {self.name} : {self.id} added to the database.")
        else:
            print(f"Planet {self.name}: {self.id} already exists in the database. update instead:")

            update_sql = f"""
            UPDATE planets SET
                id = '{self.id}',
                level = '{self.level}',
                name = '{self.name}',
                world_x = '{self.world_x}',
                world_y = '{self.world_y}',
                world_width = '{self.world_width}',
                world_height = '{self.world_height}',
                info_text = '{self.info_text_raw}',
                population_grow = '{self.population_grow}',
                alien_population = '{self.alien_population}',
                buildings_max = '{self.buildings_max}',
                building_slot_amount = '{self.building_slot_amount}',
                specials = '{self.specials}',
                type = '{self.type}',
                possible_resources = '{json.dumps(self.possible_resources)}',
                image_name_small = '{self.image_name_small}',
                image_name_big = '{self.image_name_big}',
                orbit_speed = '{self.orbit_speed}',
                orbit_object_id = '{self.orbit_object_id}',
                orbit_distance = '{self.orbit_distance}',
                atmosphere_name = '{self.atmosphere_name}',
                has_atmosphere = '{self.has_atmosphere}',
                orbit_angle = '{self.orbit_angle}'


            WHERE id = '{self.id}';
            """
            conn.execute(update_sql)

        conn.commit()
        conn.close()

    def load_from_db(self):
        """
        this is used to set the values from the editor to make shure, realtime adjustment is possible
        """
        for key, value in get_dict_from_database(id=self.id).items():
            if "[" in str(value):
                value = eval(value)
            setattr(self, key, value)



                # print("load_from_db:", key, value)


