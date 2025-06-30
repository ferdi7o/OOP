from project.player import Player


class Guild:
    def __init__(self, name: str):
        self.name = name
        self.players: list = []

    def assign_player(self, player: Player) -> str:
        if player.guild != "Unaffiliated":
            return f"Player {player.name} is in another guild."

        if player not in self.players:
            self.players.append(player)
            player.guild = self.name
            return f"Welcome player {player.name} to the guild {self.name}"

        return f"Player {player.name} is already in the guild."


    def kick_player(self, player_name: str) -> str:
        for player in self.players:
            if player.name == player_name:
                self.players.remove(player)
                player.guild = "Unaffiliated"
                return f"Player {player_name} has been kicked from the guild."
        return f"Player {player_name} is not in the guild."

    def guild_info(self) -> str:
        return f"Guild: {self.name}\n" + '\n'.join([p.player_info() for p in self.players])