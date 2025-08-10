from project.guild_halls.base_guild_hall import BaseGuildHall
from project.guild_halls.combat_hall import CombatHall
from project.guild_halls.magic_tower import MagicTower
from project.guild_members.base_guild_member import BaseGuildMember
from project.guild_members.mage import Mage
from project.guild_members.warrior import Warrior


class GuildMaster:
    def __init__(self):
        self.members: list[BaseGuildMember] = []
        self.guild_halls: list[BaseGuildHall] = []

    def add_member(self, member_type: str, member_tag: str, member_gold: int):
        valid_types = {"Warrior": Warrior, "Mage": Mage}
        if member_type not in valid_types:
            raise ValueError("Invalid member type!")

        if any(m.tag == member_tag for m in self.members):
            raise ValueError(f"{member_tag} has already been added!")

        member_class = valid_types[member_type]
        member = member_class(member_tag, member_gold)
        self.members.append(member)
        return f"{member_tag} is successfully added as {member_type}."

    def add_guild_hall(self, guild_hall_type: str, guild_hall_alias: str):
        valid_types = {"CombatHall": CombatHall, "MagicTower": MagicTower}
        if guild_hall_type not in valid_types:
            raise ValueError("Invalid guild hall type!")

        if any(g.alias == guild_hall_alias for g in self.guild_halls):
            raise ValueError(f"{guild_hall_alias} has already been added!")

        hall_class = valid_types[guild_hall_type]
        hall = hall_class(guild_hall_alias)
        self.guild_halls.append(hall)
        return f"{guild_hall_alias} is successfully added as a {guild_hall_type}."

    def assign_member(self, guild_hall_alias: str, member_type: str):
        hall = next((g for g in self.guild_halls if g.alias == guild_hall_alias), None)
        if hall is None:
            raise ValueError(f"Guild hall {guild_hall_alias} does not exist!")

        member = next((m for m in self.members if m.role == member_type), None)
        if member is None:
            raise ValueError("No available members of the type!")

        if len(hall.members) >= hall.max_member_count:
            return "Maximum member count reached. Assignment is impossible."

        self.members.remove(member)
        hall.members.append(member)
        return f"{member.tag} was assigned to {guild_hall_alias}."

    def practice_members(self, guild_hall: BaseGuildHall, sessions_number: int):
        for _ in range(sessions_number):
            for member in guild_hall.members:
                member.practice()
        total_skill_level = sum(m.skill_level for m in guild_hall.members)
        return (f"{guild_hall.alias} members have {total_skill_level} total skill level "
                f"after {sessions_number} practice session/s.")

    def unassign_member(self, guild_hall: BaseGuildHall, member_tag: str):
        member = next((m for m in guild_hall.members if m.tag == member_tag), None)
        if member is None or member.skill_level == 10:
            return "The unassignment process was canceled."

        guild_hall.members.remove(member)
        self.members.append(member)
        return f"Unassigned member {member_tag}."

    def guild_update(self, min_skill_level_value: int):
        for hall in self.guild_halls:
            hall.increase_gold(min_skill_level_value)

        sorted_halls = sorted(self.guild_halls, key=lambda h: (-len(h.members), h.alias))

        unassigned_count = len(self.members)
        total_halls = len(self.guild_halls)

        result_lines = ["<<<Guild Updated Status>>>"]
        result_lines.append(f"Unassigned members count: {unassigned_count}")
        result_lines.append(f"Guild halls count: {total_halls}")

        for hall in sorted_halls:
            if hall.members:
                sorted_tags = sorted(m.tag for m in hall.members)
                members_str = " *".join(sorted_tags)
            else:
                members_str = "N/A"

            total_gold = hall.calculate_total_gold()
            result_lines.append(f">>>Guild hall: {hall.alias}; Members: {members_str}; Total gold: {total_gold}")

        return "\n".join(result_lines)