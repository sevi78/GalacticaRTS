import pygame

from source.configuration.game_config import config
from source.economy.economy_handler import economy_handler
from source.gui.event_text import event_text


class BuildingSlot:
    """ this handles the building slot up/down grades and the tooltips
    this code is absolutely terrible, but it works :)
    Main functionalities:
    The BuildingSlot class handles the upgrade and downgrade of building slots for a selected planet in the game. It also manages the tooltips that appear when hovering over the plus and minus buttons for upgrading and downgrading the building slots.

    Methods:
    - set_building_slot_tooltip_plus: sets the tooltip text when hovering over the plus button for upgrading building slots
    - set_building_slot_tooltip_minus: sets the tooltip text when hovering over the minus button for downgrading building slots
    - reset_building_slot_tooltip: resets the tooltip text when the mouse is not hovering over the plus or minus button
    - submit_tooltip: submits the tooltip text to be displayed in the game
    - upgrade_building_slots: handles the logic for upgrading building slots, including checking if the player has enough technology and updating the planet's building slot amount and energy production
    - downgrade_building_slots: handles the logic for downgrading building slots, including updating the planet's building slot amount and energy production

    Fields:
    - minus_button_image: a dictionary containing the image for the minus button for each building slot upgrade level
    - plus_button_image: a dictionary containing the image for the plus button for each building slot upgrade level
    - tooltip: the text to be displayed in the tooltip when hovering over the plus or minus button
    - plus_just_hovered: a boolean indicating whether the plus button was just hovered over
    - minus_just_hovered: a boolean indicating whether the minus button was just hovered over
    """

    def __init__(self):
        self.minus_button_image = {}
        self.plus_button_image = {}
        self.tooltip = ""
        self.plus_just_hovered = False
        self.minus_just_hovered = False

    def set_building_slot_tooltip_plus(self):
        # if not planet selected, do nothing
        if not self.parent.selected_planet:
            return

        planet = self.parent.selected_planet
        upgrades = planet.economy_agent.building_slot_upgrades
        consumption = planet.economy_agent.building_slot_upgrade_energy_consumption
        prices = planet.economy_agent.building_slot_upgrade_prices
        max_ = len(planet.economy_agent.building_slot_upgrade_energy_consumption) - 2

        # check for mouse collision with image
        for button_name, image_rect in self.plus_button_image.items():
            if button_name == "plus_icon":

                if image_rect.collidepoint(pygame.mouse.get_pos()):
                    self.hover = True
                    if not self.plus_just_hovered:
                        self.plus_just_hovered = True
                else:
                    self.hover = False

        # on hover set tooltip
        if self.hover:
            # if not max upgrade reached
            if upgrades <= max_:
                self.tooltip = f"Upgrade from {planet.economy_agent.building_slot_amount} building slots to " \
                               f"{planet.economy_agent.building_slot_amount + 1}? this will cost you " \
                               f"{prices[upgrades]}" \
                               f" technology! it will reduce the energy production by" \
                               f" {consumption[upgrades + 1]}"
            else:
                self.tooltip = f"you have reached the maximum {max} of possible building slot upgrades !"

        self.submit_tooltip()

    def set_building_slot_tooltip_minus(self):
        # if not planet selected, do nothing
        if not self.parent.selected_planet:
            return

        planet = self.parent.selected_planet
        upgrades = planet.economy_agent.building_slot_upgrades
        consumption = planet.economy_agent.building_slot_upgrade_energy_consumption
        min_ = 0
        self.tooltip = ""

        # check for mouse collision with image
        for button_name, image_rect in self.minus_button_image.items():
            if button_name == "minus_icon":

                if image_rect.collidepoint(pygame.mouse.get_pos()):
                    self.hover = True
                    if not self.minus_just_hovered:
                        self.minus_just_hovered = True
                else:
                    self.hover = False

        # on hover set tooltip
        if self.hover:
            # if not max upgrade reached
            if planet.economy_agent.building_slot_amount >= min_ + 1:
                self.tooltip = f"Downgrade from {planet.economy_agent.building_slot_amount} building slots to " \
                               f"{planet.economy_agent.building_slot_amount - 1}? this will not give anything back,  " \
                               f" but it will increase the energy production by" \
                               f" {consumption[upgrades]}"
            else:
                self.tooltip = f"you have reached the minimum{min_} of possible building slot downgrades !"

        self.submit_tooltip()

    def reset_building_slot_tooltip(self):
        if not self.parent.selected_planet:
            return

        if not self.parent.selected_planet.explored:
            return

        if self._hidden:
            return

        if not self.plus_button_image["plus_icon"].collidepoint(pygame.mouse.get_pos()):
            if self.plus_just_hovered:
                config.tooltip_text = ""
                self.plus_just_hovered = False

        if not self.minus_button_image["minus_icon"].collidepoint(pygame.mouse.get_pos()):
            if self.minus_just_hovered:
                config.tooltip_text = ""
                self.minus_just_hovered = False

    def submit_tooltip(self):
        if self.tooltip != "":
            if self.tooltip != config.tooltip_text:
                config.tooltip_text = self.tooltip

    def upgrade_building_slots(self, events, player):
        planet = self.parent.selected_planet
        if not planet.explored or planet.type == "sun":
            return

        do_upgrade = False

        # check if not max is reached
        if planet.economy_agent.building_slot_upgrades <= len(planet.economy_agent.building_slot_upgrade_prices) - 2:
            # now get the next price
            price = planet.economy_agent.building_slot_upgrade_prices[planet.economy_agent.building_slot_upgrades]

            # on hover and click, do upgrade
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button_name, image_rect in self.plus_button_image.items():
                        if button_name == "plus_icon":
                            if image_rect.collidepoint(pygame.mouse.get_pos()):
                                do_upgrade = True

        # max upgrades reached, exit function
        else:
            event_text.set_text(f"maximum {planet.economy_agent.building_slot_upgrades} building slots reached!", sender=player.owner)
            return

        # if do_upgrade, set values
        if not do_upgrade:
            return

        # if enough technology
        if player.stock["technology"] - price > 0:
            event_text.set_text(f"Upgraded from {planet.economy_agent.building_slot_amount} building slots to {planet.economy_agent.building_slot_amount + 1}!", sender=player.owner)
            # if not max reached
            if planet.economy_agent.building_slot_upgrades < len(planet.economy_agent.building_slot_upgrade_prices.items()):
                planet.economy_agent.building_slot_amount += 1
                planet.economy_agent.building_slot_upgrades += 1
                # TODO: possble error here, shouldnt it be player.stock["technology] -= price ????
                player.stock["technology"] -= price
        else:
            event_text.set_text(f"not enough technology to upgrade building slot ! you have {player.stock['technology']}, but you will need {price}", sender=player.owner)

        # finally calculate new productions
        planet.economy_agent.calculate_production()
        economy_handler.calculate_global_production(player)

    def downgrade_building_slots(self, events, player):
        planet = self.parent.selected_planet
        if not planet.explored or planet.type == "sun":
            return

        do_downgrade = False

        # check if not min is reached
        if planet.economy_agent.building_slot_upgrades >= 0:
            # on hover and click, do upgrade
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button_name, image_rect in self.minus_button_image.items():
                        if button_name == "minus_icon":
                            if image_rect.collidepoint(pygame.mouse.get_pos()):
                                do_downgrade = True

        # min upgrades reached, exit function
        else:
            event_text.set_text(f"minimum {0} building slots reached!", sender=player.owner)
            return

        # if do_upgrade, set values
        if not do_downgrade:
            return

        event_text.set_text(f"Downgraded from {planet.economy_agent.building_slot_amount} building slots to {planet.economy_agent.building_slot_amount - 1}!",sender=player.owner)

        # if not min reached
        if planet.economy_agent.building_slot_amount > 0:
            planet.economy_agent.building_slot_amount -= 1
            if planet.economy_agent.building_slot_upgrades > 0:
                planet.economy_agent.building_slot_upgrades -= 1

        # finally calculate new productions
        planet.economy_agent.calculate_production()
        economy_handler.calculate_global_production(player)
