from abc import ABC, abstractmethod

from project.products.base_product import BaseProduct


class BaseStore(ABC):
    def __init__(self, name:str, location:str, capacity:int):
        self.name = name
        self.location = location
        self.capacity = capacity
        self.products: list[BaseProduct] = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if value == "":
            raise ValueError("Store name cannot be empty!")
        self.__name = value

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value):
        if len(value) != 3 or " " in value:
            raise ValueError("Store location must be 3 chars long!")
        self.__location = value

    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, value):
        if value < 0:
            raise ValueError("Store capacity must be a positive number or 0!")
        self.__capacity = value

    def get_estimated_profit(self):
        profit = sum(produc.price for produc in self.products) * 0.10 # 10%
        return f"Estimated future profit for {len(self.products)} products is {profit:.2f}"

    @property
    @abstractmethod
    def store_type(self):
        pass

    def store_stats(self):
        result = [f"Store: {self.name}, location: {self.location}, available capacity: {self.capacity}",
                  self.get_estimated_profit(),
                  f"**{str(self)} for sale:"]

        products = {}
        for product in self.products:
            if product.model not in products:
                products[product.model] = {"count": 0, "total_price": 0}
            products[product.model]["count"] += 1
            products[product.model]["total_price"] += product.price

        for model in sorted(products.keys()):
            count = products[model]["count"]
            total_price = products[model]["total_price"] / count
            result.append(f"{model}: {count}pcs, average price: {total_price:.2f}")

        return "\n".join(result).strip()

