from project.product import Product


class Food(Product):
    def __init__(self, name, price, grams: float):
        super().__init__(name, price)
        self.__grams = grams

    @property
    def milliliters(self):
        return self.__grams

    @property
    def grams(self):
        return self.__grams