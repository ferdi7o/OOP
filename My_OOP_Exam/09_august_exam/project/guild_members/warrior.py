from project.guild_members.base_guild_member import BaseGuildMember


class Warrior(BaseGuildMember):
    ROLE = 'Warrior'
    SKILL_LEVEL = 2

    def __init__(self, tag: str, gold: int):
        super().__init__(tag, gold, self.ROLE, self.SKILL_LEVEL)

    def practice(self):
        self.skill_level = min(self.skill_level + 2, 10)