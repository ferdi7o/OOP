from project.robots.base_robot import BaseRobot
from project.robots.female_robot import FemaleRobot
from project.robots.male_robot import MaleRobot

from project.services.base_service import BaseService
from project.services.main_service import MainService
from project.services.secondary_service import SecondaryService


class RobotsManagingApp:
    def __init__(self):
        self.robots: list[BaseRobot] = []
        self.services: list[BaseService] = []

    def add_service(self, type: str, name: str):
        if type == "MainService":
            service = MainService(name)
        elif type == "SecondaryService":
            service = SecondaryService(name)
        else:
            raise Exception("Invalid service type!")

        self.services.append(service)
        return f"{type} is successfully added."

    def add_robot(self, type: str, name: str, kind: str, price: float):
        if type == "MaleRobot":
            robot = MaleRobot(name, kind, price)
        elif type == "FemaleRobot":
            robot = FemaleRobot(name, kind, price)
        else:
            raise Exception("Invalid robot type!")

        self.robots.append(robot)
        return f"{type} is successfully added."

    def add_robot_to_service(self, robot_name: str, service_name: str):
        robot = next(r for r in self.robots if r.name == robot_name)
        service = next(s for s in self.services if s.name == service_name)

        if (robot.__class__.__name__ == "MaleRobot" and service.__class__.__name__ != "MainService") or \
                (robot.__class__.__name__ == "FemaleRobot" and service.__class__.__name__ != "SecondaryService"):
            return "Unsuitable service."

        if len(service.robots) >= service.capacity:
            raise Exception("Not enough capacity for this robot!")

        self.robots.remove(robot)
        service.robots.append(robot)
        return f"Successfully added {robot_name} to {service_name}."

    def remove_robot_from_service(self, robot_name: str, service_name: str):
        service = next(s for s in self.services if s.name == service_name)
        robot = next((r for r in service.robots if r.name == robot_name), None)

        if robot is None:
            raise Exception("No such robot in this service!")

        service.robots.remove(robot)
        self.robots.append(robot)
        return f"Successfully removed {robot_name} from {service_name}."

    def feed_all_robots_from_service(self, service_name: str):
        service = next(s for s in self.services if s.name == service_name)

        for robot in service.robots:
            robot.eating()

        return f"Robots fed: {len(service.robots)}."

    def service_price(self, service_name: str):
        service = next(s for s in self.services if s.name == service_name)
        total_price = sum(r.price for r in service.robots)
        return f"The value of service {service_name} is {total_price:.2f}."

    def __str__(self):
        result = []
        for service in self.services:
            result.append(service.details())
        return "\n".join(result)
