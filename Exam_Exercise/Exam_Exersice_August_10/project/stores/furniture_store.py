from project.stores.base_store import BaseStore


class FurnitureStore(BaseStore):
    CAPACITY = 50


    def __init__(self, name, location):
        super().__init__(name, location, self.CAPACITY)

    def store_type(self):
        return "FurnitureStore"

    def __str__(self):
        return "Furniture"