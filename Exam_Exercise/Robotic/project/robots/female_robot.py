from project.robots.base_robot import BaseRobot


class FemaleRobot(BaseRobot):
    INITAL_WEIGHT = 7

    def __init__(self, name:str, kind:str, price:float):
        super().__init__(name, kind, price, self.INITAL_WEIGHT)

    def eating(self):
        self.INITAL_WEIGHT += 1
        return self.INITAL_WEIGHT