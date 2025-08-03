from project.stores.base_store import BaseStore


class ToyStore(BaseStore):
    CAPACITY = 100

    def __init__(self, name, location):
        super().__init__(name, location, self.CAPACITY)

    def store_type(self):
        return "ToyStore"

    def __str__(self):
        return "Toys"

