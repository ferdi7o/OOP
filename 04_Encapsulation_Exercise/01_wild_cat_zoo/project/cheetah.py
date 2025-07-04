from project.animal import Animal

class Cheetah(Animal):
    def __init__(self, name: str, gender: str, age: int) -> None:
        super().__init__(name, gender, age, money_for_care=60)