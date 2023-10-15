create_planet_table_sql = """

CREATE TABLE IF NOT EXISTS planets (
	id integer PRIMARY KEY,
	level integer NOT NULL,
	name text NOT NULL,
	x integer NOT NULL,
	y integer NOT NULL,
	info_text text NOT NULL,
	population_grow float NOT NULL,
	alien_population integer NOT NULL,
	buildings_max integer NOT NULL,
	building_slot_amount integer NOT NULL,
	specials text,
	type text NOT NULL,
	possible_resources text NOT NULL, 
	image_name_small text NOT NULL,
	image_name_big text NOT NULL,
	orbit_speed float NOT NULL
	);
"""

create_ship_table_sql = f""

insert_planet_sql = """
INSERT INTO planets (id, level, name, x,y,info_text, population_grow, alien_population, buildings_max, 
building_slot_amount, specials, type, possible_resources, image_name_small, image_name_big, orbit_speed )
VALUES( 0,1,"test", 100,100,"info", 0.1,1000,10,3,"None","planet","['water', 'food', 'minerals']",
"GIN V.S.X.O._80x80.png", "GIN V.S.X.O._150x150.png", 0.007);
"""

# """
# #conn.execute("ALTER Table planets ADD COLUMN orbit_distance decimal; ")
#         #orbit_object_id = 0
#         #conn.execute(f"UPDATE planets SET orbit_object_id = {orbit_object_id} where id = {self.id}")
#
#         # # Create the planets table if it does not exist
#         # create_table_sql = """
#         # CREATE TABLE IF NOT EXISTS planets (
#         #     id INTEGER PRIMARY KEY,
#         #     level INTEGER,
#         #     name TEXT,
#         #     x INTEGER,
#         #     y INTEGER,
#         #     width INTEGER,
#         #     height INTEGER,
#         #     info_text TEXT,
#         #     population_grow INTEGER,
#         #     alien_population INTEGER,
#         #     buildings_max INTEGER,
#         #     building_slot_amount INTEGER,
#         #     specials TEXT,
#         #     type TEXT,
#         #     possible_resources TEXT,
#         #     image_name_small TEXT,
#         #     image_name_big TEXT,
#         #     orbit_speed REAL
#         # );
#         # """
#         # insert(conn, create_table_sql)
#
#         # conn.execute("ALTER Table planets ADD COLUMN width integer; ")
#         # conn.execute("ALTER Table planets ADD COLUMN height integer; ")
#
#         # Check if the planet already exists in the database
#         #select_sql = f"SELECT * FROM planets WHERE id = '{self.id}'"
#
#
# """
