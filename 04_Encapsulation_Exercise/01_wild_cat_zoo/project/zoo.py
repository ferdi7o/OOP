from project.animal import Animal
from project.worker import Worker


class Zoo:
    def __init__(self, name: str, budget: int, animal_capacity: int, workers_capacity: int):
        self.name = name
        self.__budget = budget
        self.__animal_capacity = animal_capacity
        self.__workers_capacity = workers_capacity
        self.animals: list = []
        self.workers: list = []

    def add_animal(self, animal: Animal, price: int):
        if price <= self.__budget and self.__animal_capacity > len(self.animals):
            self.__budget -= price
            self.animals.append(animal)
            return f"{animal.name} the {animal.__class__.__name__} added to the zoo"
        if self.__budget < price:
            return "Not enough budget"
        return "Not enough space for animal"

    def hire_worker(self, worker: Worker):
        if self.__workers_capacity >= len(self.workers):
            return f"{worker.name} the {worker.__class__.__name__} hired successfully"
        return "Not enough space for worker"

    def fire_worker(self, worker_name: Worker):
        if worker_name in self.workers:
            self.workers.remove(worker_name)
            return f"{worker_name} fired successfully"
        return f"There is no {worker_name} in the zoo"

    def pay_workers(self):
        total_salary = sum(w.salary for w in self.workers)
        if total_salary > self.__budget:
            return "You have no budget to pay your workers. They are unhappy"
        self.__budget -= total_salary
        return f"You payed your workers. They are happy. Budget left: {self.__budget}"

    def tend_animals(self):
        total_money_for_care = sum(a.money_for_care for a in self.animals)
        if total_money_for_care > self.__budget:
            return "You have no budget to tend the animals. They are unhappy."
        self.__budget -= total_money_for_care
        return f"You tended all the animals. They are happy. Budget left: {self.__budget}"

    def profit(self, amount: int) -> None:
        self.__budget += amount

    def animals_status(self):
         return self.__printing_status(self.animals, "Lions", "Tigers", "Cheetahs")

    def workers_status(self):
        return self.__printing_status(self.workers, "Keepers", "Caretakers", "Vets")

    @staticmethod
    def __printing_status(data_list: list[Animal | Worker], *args):
        elements = {arg: [] for arg in args}
        for el in elements:
            elements[el.__class__.__name__].append(repr(el))
        result = [f"You have {len(data_list)} {str(data_list[0].__class__.__bases__.__name__).lower()}s\n"]
        for key, value in elements.items():
            result += f"----- {len(value)} {key}s:\n'{'\n'.join([str(v) for v in elements.values()])}"
        return result