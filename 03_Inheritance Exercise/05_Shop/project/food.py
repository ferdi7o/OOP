from project.product import Product


class Food(Product):
    def __init__(self, name: str, quuantity= 15):
        super().__init__(name, quuantity)
