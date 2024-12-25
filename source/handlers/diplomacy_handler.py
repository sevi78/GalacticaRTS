from source.configuration.game_config import config
from source.handlers.orbit_handler import set_orbit_object_id
from source.handlers.pan_zoom_sprite_handler import sprite_groups


class DiplpmacyHandler:
    def __init__(self):
        self.enemy_index = -1
        self.player_index = -1

    def set_enemy_and_player(self, enemy_index: int, player_index: int) -> None:
        """
        Sets the enemy and player indices for the diplomacy handler.

        Args:
            enemy_index (int): The index of the enemy player.
            player_index (int): The index of the player.

        Returns:
            None: This function does not return anything.

        This function updates the enemy and player indices for the diplomacy handler. It also updates the text and image
        of the diplomacy edit based on the current peace or war status between the enemy and player.
        Finally, it updates the diplomacy button image in the player edit.

        Note:
            - This function assumes that the `config` module is imported and that the `app` attribute of the `config`
             module contains the necessary objects for updating the diplomacy edit and player edit.

        """
        diplomacy_edit = config.app.diplomacy_edit
        self.player_index = player_index
        self.enemy_index = enemy_index

        if self.player_index != 0:
            name_text = f"{config.app.players[self.player_index].name} is"
        else:
            name_text = "You are"

        if self.is_in_peace(self.enemy_index, self.player_index):
            diplomacy_edit.text = f"{name_text} in peace with {config.app.players[self.enemy_index].name}"
        else:
            diplomacy_edit.text = f"{name_text} in war with {config.app.players[self.enemy_index].name}"

        diplomacy_edit.set_enemy_image()

        # update player_edit
        config.app.player_edit.update_diplomacy_button_image()

    def is_in_peace(self, player_index: int, opponent_index: int) -> bool:
        """
        checks if any index is in players enemies list of indexes(int),
        if any indexes found, this means war, else peace
        """
        if player_index != -1:
            if opponent_index in config.app.players[player_index].enemies:
                return False
            else:
                return True
        return True

    def update_diplomacy_status(self, status: str) -> None:
        """
        Updates the diplomacy status between two players to either peace or war based on the 'status' parameter.
        :param status: A string that should be either 'peace' or 'war' to set the respective status.
        """

        if config.app.game_client.connected:
            config.app.game_client.send_message({
                "f": "update_diplomacy_status",
                "player_index": self.player_index,
                "enemy_index": self.enemy_index,
                "status": status
                })
        else:
            self.handle_update_diplomacy_status(self.player_index, self.enemy_index, status)

    def handle_update_diplomacy_status(self, player_index, enemy_index, status):
        diplomacy_edit = config.app.diplomacy_edit
        player_enemies = config.app.players[player_index].enemies
        enemy_enemies = config.app.players[enemy_index].enemies

        if status == 'peace':
            if not self.is_in_peace(player_index, enemy_index):
                if enemy_index in player_enemies:
                    player_enemies.remove(enemy_index)
                if player_index in enemy_enemies:
                    enemy_enemies.remove(player_index)

        elif status == 'war':
            if self.is_in_peace(player_index, enemy_index):
                player_enemies.append(enemy_index)
                enemy_enemies.append(player_index)

        # Reset values for display and hide editor
        self.set_enemy_and_player(enemy_index, player_index)
        diplomacy_edit.hide()

        # update orbiting ships
        self.update_orbiting_ships(status, player_index)

    def update_orbiting_ships(self, status: str, player_index: int) -> None:
        """
        updates orbiting ships:
        - peace -> set orbit object
        - war -> set enemy
        :param status: 'peace' or 'war'
        :param player_index: player index
        """
        # check for all ships
        for ship in sprite_groups.ships.sprites():
            # check if ship belongs to player of the orbiting planet
            if ship.owner == player_index:
                if status == 'peace':
                    # check if ship has an enemy
                    if ship.enemy:
                        # get the enemy, we need to store it locally because it will be removed in the property
                        enemy = ship.enemy

                        # delete the enemy
                        ship.enemy = None

                        # set the orbit object
                        set_orbit_object_id(ship, enemy.id)

                if status == 'war':
                    # check if ship has an orbit object
                    if ship.orbit_object:
                        # get the orbit object, we need to store it locally because it will be removed in the property
                        orbit_object = ship.orbit_object

                        # delete the orbit object
                        ship.orbit_object = None

                        # set the enemy
                        ship.enemy = orbit_object


diplomacy_handler = DiplpmacyHandler()
