from source.configuration.game_config import config


class DiplpmacyHandler:
    def __init__(self):
        self.enemy_index = None
        self.player_index = None

    def set_enemy_and_player(self, enemy_index: int, player_index: int) -> None:
        diplomacy_edit = config.app.diplomacy_edit
        self.player_index = player_index
        self.enemy_index = enemy_index

        if self.is_in_peace(self.enemy_index, self.player_index):
            diplomacy_edit.text = f"you are in peace with {config.app.players[self.enemy_index].name}."
        else:
            diplomacy_edit.text = f"You are in war with {config.app.players[self.enemy_index].name}"

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
        diplomacy_edit = config.app.diplomacy_edit
        player_enemies = config.app.players[self.player_index].enemies
        enemy_enemies = config.app.players[self.enemy_index].enemies

        if status == 'peace':
            if not self.is_in_peace(self.player_index, self.enemy_index):
                player_enemies.remove(self.enemy_index)
                enemy_enemies.remove(self.player_index)
        elif status == 'war':
            if self.is_in_peace(self.player_index, self.enemy_index):
                player_enemies.append(self.enemy_index)
                enemy_enemies.append(self.player_index)

        # Reset values for display and hide editor
        self.set_enemy_and_player(self.enemy_index, self.player_index)
        diplomacy_edit.hide()


diplomacy_handler = DiplpmacyHandler()
