import pygame

import source.handlers.weapon_handler
from source.factories.planet_factory import planet_factory
from source.game_play import enemy_handler
from source.configuration import global_params
from source.handlers.pan_zoom_sprite_handler import sprite_groups


class Cheat:
    def cheat_ship(self):
        if self.ship:
            self.ship.energy = 10000

    def cheat_planetary_defence(self, weapon):
        if not self.selected_planet:
            return

        for i in planet_factory.get_all_planets(["planet", "moon"]):
            i.buildings.append(weapon)



    def cheat_population(self):
        for i in sprite_groups.planets:
            i.population = 100000

    def cheat_resources_and_population(self, value):
        self.player.energy += value
        self.player.food += value
        self.player.minerals += value
        self.player.water += value
        self.player.technology += value * 10
        self.player.population += value / 4

        for i in sprite_groups.planets:
            i.population += value / 4

    def explore_all(self):
        for p in sprite_groups.planets:
            p.explored = True
        for pl in sprite_groups.planets:
            pl.get_explored()
            pl.explored = True

    def cheat_missile(self):
        if not self.selected_planet:
            return
        # self.selected_planet.buildings.append("missile")

        for i in sprite_groups.planets:
            i.buildings.append("missile")


    def cheat_ufo(self):
        if not self.selected_planet:
            return
        ufo = enemy_handler.enemy_handler.spawn_ufo(self.selected_planet)
        source.handlers.weapon_handler.launch_missile(self.selected_planet, ufo)

    def cheat(self, events):
        # ignore all inputs while any text input is active
        if global_params.text_input_active:
            return
        """cheat you bloody cheater :) """
        for event in events:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and not pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.cheat_resources_and_population(10000)
                    self.cheat_planetary_defence("electro magnetic impulse")
                    self.cheat_ship()
                    #self.cheat_missile()

                    # self.cheat_ufo()

                    self.explore_all()


                    # self.cheat_population()
                    # self.explore_all()

                    # print (building_factory.get_a_list_of_building_names_with_build_population_minimum_bigger_than(1000))
