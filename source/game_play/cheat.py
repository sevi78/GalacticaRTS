import copy
import random

import pygame

import source.handlers.weapon_handler
from source.configuration.game_config import config
from source.factories.planet_factory import planet_factory
from source.factories.weapon_factory import weapon_factory
from source.game_play import enemy_handler
from source.handlers.pan_zoom_sprite_handler import sprite_groups


class Cheat:
    def cheat_ship(self):
        if self.ship:
            self.ship.energy = 10000

    def cheat_ships(self):
        for i in self.players:
            if not i == 0:
                planets = [_ for _ in sprite_groups.planets.sprites() if _.owner == i]
                if planets:
                    planet = random.choice(planets)
                    x, y = planet.world_y, planet.world_y
                else:
                    return

                ship = self.ship_factory.create_ship(
                        "spaceship",
                        x,
                        y,
                        config.app,
                        {"rocket": copy.deepcopy(weapon_factory.get_weapon("rocket"))},
                        data={"owner": i, "autopilot": True}),

    def cheat_planetary_defence(self, weapon):
        if not self.selected_planet:
            return

        for i in planet_factory.get_all_planets(["planet", "moon"]):
            i.economy_agent.buildings.append(weapon)

    def cheat_population(self, value):
        for i in sprite_groups.planets:
            i.economy_agent.population += value

    def cheat_resources(self, value):
        for key, v in self.player.stock.items():
            self.player.stock[key] += value

    def cheat_resource(self, resource, value, **kwargs):

        """
        why is it going into the else condition even player_index is not None ?
        """
        player_index = kwargs.get("player_index", None)

        if player_index is not None:
            # setattr(self.players[player_index], resource, getattr(self.players[player_index], resource) + value)
            self.players[player_index].stock[resource] += value

        else:
            for i in self.players:
                # setattr(self.players[i], resource, getattr(self.players[i], resource) + value)
                self.players[i].stock[resource] += value

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
        for pl in sprite_groups.planets:
            pl.get_explored(0)
            pl.explored = True

    def cheat_missile(self):
        if not self.selected_planet:
            return
        # self.selected_planet.buildings.append("missile")

        for i in sprite_groups.planets:
            i.economy_agent.buildings.append("missile")

    def spawn_ufo(self):
        if not self.selected_planet:
            return
        ufo = enemy_handler.enemy_handler.spawn_ufo(self.selected_planet)

    def cheat_ufo(self):
        if not self.selected_planet:
            return
        ufo = enemy_handler.enemy_handler.spawn_ufo(self.selected_planet)
        source.handlers.weapon_handler.launch_missile(self.selected_planet, ufo)

    def cheat_level_success(self):
        for key, value in self.level_handler.level_successes.items():
            self.level_handler.level_successes[key] = True
            self.level_select.update_icons()

    def cheat_all(self):
        # self.cheat_resources(10000)
        # self.cheat_ship()
        self.cheat_population(10000.0)
        # self.explore_all()
        # self.cheat_level_success()

    def test_attacking(self):
        if config.app.ship:
            config.app.ship.energy = 10
        for i in sprite_groups.planets:
            i.economy_agent.buildings.append("electro magnetic impulse")
            i.economy_agent.buildings.append("solar panel")
        self.cheat_population(100000.0)
        self.spawn_ufo()
        self.cheat_resources(100000.0)
        config.app.map_panel.set_visible()


    def cheat(self, events):
        # ignore all inputs while any text input is active
        if config.text_input_active:
            return
        """cheat you bloody cheater :) """
        for event in events:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and not pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # self.cheat_resources_and_population(100)
                    # # self.cheat_resources(10000)
                    # # self.cheat_population(1000)
                    # # self.cheat_planetary_defence("electro magnetic impulse")
                    # self.cheat_ship()
                    # # self.cheat_missile()
                    #
                    # # self.cheat_ufo()
                    #
                    # self.explore_all()
                    # self.cheat_level_success()
                    #
                    # # self.cheat_population()
                    # # self.explore_all()
                    # self.cheat_all()
                    self.test_attacking()
                    # print (building_factory.get_a_list_of_building_names_with_build_population_minimum_bigger_than(1000))
