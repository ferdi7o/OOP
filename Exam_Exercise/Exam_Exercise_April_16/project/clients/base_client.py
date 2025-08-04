from abc import ABC, abstractmethod


class BaseClient(ABC):
    MEMBERSHIP_TYPE = ["Regular", "VIP"]

    def __init__(self, name:str, membership_type:str):
        self.name = name
        self.membership_type = membership_type
        self.points = 0

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if value == "" or value == " ":
            raise ValueError("Client name should be determined!")
        self.__name = value

    @property
    def membership_type(self):
        return self.__membership_type

    @membership_type.setter
    def membership_type(self, value):
        if value not in self.MEMBERSHIP_TYPE:
            raise ValueError("Invalid membership type. Allowed types: Regular, VIP.")
        self.__membership_type = value

    def earning_points(self, order_amount:float):
        self.points += order_amount
        return self.points

    def apply_discount(self):
