from source.interfaces.interface import InterfaceData
from source.multimedia_library.sounds import sounds
from source.pan_zoom_sprites.pan_zoom_ship_classes.pan_zoom_ship import PanZoomShip

"""no longer used"""
class Spaceship(PanZoomShip, InterfaceData):
    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomShip.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.name = "spaceship"
        self.hum = sounds.hum1
        self.sound_channel = 1

        self.speed = 1.5
        self.speed_max = 2.5
        self.energy_max = 10000
        self.energy = 10000
        self.energy_use = 0.0005
        self.energy_reload_rate = 0.1
        # self.move_stop = 0
        self.energy_warning_level = 500
        self.noenergy_image_x = 0
        self.noenergy_image_y = -self.get_screen_height()
        self.rank_image_x = 0
        self.rank_image_y = -self.get_screen_height() / 1.5

        self.food_max = 500
        self.minerals_max = 200
        self.technology_max = 500
        self.minerals_max = 300
        self.water_max = 400
        self.crew = 7

        self.crew_members = ["john the cook", "jim the board engineer", "stella the nurse", "sam the souvenir dealer",
                             "jean-jaques the artist", "Nguyen thon ma, the captain", "dr. Hoffmann the chemist"]

        # fog of war
        self.fog_of_war_radius = 100

        # tooltip
        self.set_tooltip()

        # gun
        self.current_weapon = self.all_weapons["laser"]
        self.gun_power = 5
        self.gun_power_max = 25

        InterfaceData.__init__(self, self.interface_variable_names)

        # get data from ship_settings
        self.setup()


class Cargoloader(PanZoomShip, InterfaceData):
    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        PanZoomShip.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.name = "cargoloader"
        self.hum = sounds.hum2
        self.sound_channel = 2

        self.speed = 1.0
        self.speed_max = 5.0
        self.energy_max = 20000
        self.energy = 15000
        self.energy_use = 0.001
        self.energy_reload_rate = 0.05
        # self.move_stop = 0
        self.energy_warning_level = 500
        self.noenergy_image_x = 0
        self.noenergy_image_y = -self.get_screen_height() / 2
        self.rank_image_x = 0
        self.rank_image_y = -self.get_screen_height() / 2.4

        self.food_max = 1500
        self.minerals_max = 2000
        self.technology_max = 1500
        self.minerals_max = 1000
        self.water_max = 1000

        self.crew = 7
        self.crew_members = ["john the cook", "jim the board engineer", "stella the nurse", "sam the souvenir dealer",
                             "jean-jaques the artist", "Nguyen thon ma, the captain", "dr. Hoffmann the chemist"]

        # fog of war
        self.fog_of_war_radius = 50

        # tooltip
        self.set_tooltip()

        # gun
        self.current_weapon = self.all_weapons["phaser"]
        self.gun_power = 1
        self.gun_power_max = 5

        # interface
        InterfaceData.__init__(self, self.interface_variable_names)

        # get data from ship_settings
        self.setup()


class Spacehunter(PanZoomShip, InterfaceData):
    def __init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs):
        # PanZoomShipInterfaceData.__init__(self)
        PanZoomShip.__init__(self, win, x, y, width, height, pan_zoom, image_name, **kwargs)
        self.name = "spacehunter"
        self.hum = sounds.hum3
        self.sound_channel = 3

        self.speed = 2.5
        self.speed_max = 5.0
        self.energy_max = 5000
        self.energy = 5000
        self.energy_use = 0.0015
        self.energy_reload_rate = 0.15
        self.energy_warning_level = 500
        self.noenergy_image_x = 0
        self.noenergy_image_y = -self.get_screen_height()
        self.rank_image_x = 0
        self.rank_image_y = -self.get_screen_height() / 1.5

        self.food_max = 200
        self.minerals_max = 200
        self.technology_max = 150
        self.minerals_max = 100
        self.water_max = 100

        self.crew = 7
        self.crew_members = ["john the cook", "jim the board engineer", "stella the nurse", "sam the souvenir dealer",
                             "jean-jaques the artist", "Nguyen thon ma, the captain", "dr. Hoffmann the chemist"]

        # fog of war
        self.fog_of_war_radius = 30

        # tooltip
        self.set_tooltip()

        # gun
        self.current_weapon = self.all_weapons["rocket"]
        self.gun_power = 25
        self.gun_power_max = 125

        # interface
        InterfaceData.__init__(self, self.interface_variable_names)

        # get data from ship_settings
        self.setup()
