from abc import ABC, abstractmethod


class BaseGuildHall(ABC):
    def __init__(self, alias: str):
        self.alias = alias
        self.members: list = []

    @property
    def alias(self):
        return self.__alias

    @alias.setter
    def alias(self, value):
        stripped = value.strip()
        if len(stripped) < 2 or \
                not all(char.isalpha() or char.isspace() for char in stripped):
            raise ValueError("Guild hall alias is invalid!")
        self.__alias = stripped

    @property
    @abstractmethod
    def max_member_count(self):
        pass

    def calculate_total_gold(self):
        if not self.members:
            return 0
        return sum(member.gold for member in self.members)

    def status(self):
        if self.members:
            tags = sorted(member.tag for member in self.members)
            members_list = ' *'.join(tags)
        else:
            members_list = 'N/A'

        return (f"Guild hall: {self.alias}; Members: {members_list}; "
                f"Total gold: {self.calculate_total_gold()}")

    @abstractmethod
    def increase_gold(self, min_skill_level_value: int):
        pass
