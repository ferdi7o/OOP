from project.clients.base_client import BaseClient


class BusinessClient(BaseClient):
    def __init__(self, name, phone_number):
        super().__init__(name, phone_number)

    def update_discount(self):
        if self.total_orders >= 2:
            self.discount = 10.0
        else:
            self.discount = 0