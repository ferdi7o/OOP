from project.clients.base_client import BaseClient
from project.clients.business_client import BusinessClient
from project.clients.regular_client import RegularClient
from project.plants.base_plant import BasePlant
from project.plants.flower import Flower
from project.plants.leaf_plant import LeafPlant


class FlowerShopManager:
    VALID_TYPES = {"Flower": Flower, "LeafPlant": LeafPlant}
    VALID_CLIENTS = {"RegularClient": RegularClient, "BusinessClient": BusinessClient}

    def __init__(self):
        self.income: float = 0.0
        self.plants: list[BasePlant] = []
        self.clients: list[BaseClient] = []

    def add_plant(self, plant_type: str, plant_name: str, plant_price: float, plant_water_needed: int, plant_extra_data: str):
        if plant_type not in self.VALID_TYPES:
            raise ValueError("Unknown plant type!")
        plant = self.VALID_TYPES[plant_type](plant_name, plant_price, plant_water_needed, plant_extra_data)
        self.plants.append(plant)
        return f"{plant_name} is added to the shop as {plant_type}."

    def add_client(self, client_type: str, client_name: str, client_phone_number: str):
        if client_type not in self.VALID_CLIENTS:
            raise ValueError("Unknown client type!")
        client = self.VALID_CLIENTS[client_type](client_name, client_phone_number)
        for c in self.clients:
            if c.phone_number == client_phone_number:
                raise ValueError("This phone number has been used!")
        self.clients.append(client)
        return f"{client_name} is successfully added as a {client_type}."

    def sell_plants(self, client_phone_number: str, plant_name: str, plant_quantity: int):
        for c in self.clients:
            if c.phone_number == client_phone_number:
                break
        else:
            raise ValueError("Client not found!")

        plants = [p for p in self.plants if p.name == plant_name]
        if not plants:
            raise ValueError("Plants not found!")

        if plant_quantity > len(plants):
            return "Not enough plant quantity."

        plants = plants[:plant_quantity]
        total_sum = sum([p.price for p in plants])
        total_sum_with_discount = total_sum - c.discount * total_sum /100

        self.income += total_sum_with_discount

        for p in plants:
            self.plants.remove(p)

        c.update_total_orders()
        c.update_discount()
        return f"{plant_quantity}pcs. of {plant_name} plant sold for {total_sum_with_discount:.2f}"

    def remove_plant(self, plant_name: str):
        plants = [plant for plant in self.plants if plant.name == plant_name]
        if not plants:
            return "No such plant name."
        plant = plants[0]
        self.plants.remove(plant)
        return f"Removed {plant.plant_details()}"

    def remove_clients(self):
        clients_no_ordered = [c for c in self.clients if c.total_orders == 0]
        for c in clients_no_ordered:
            self.clients.remove(c)
        return f"{len(clients_no_ordered)} client/s removed."

    def shop_report(self):
        unsold_flowers = {}
        for plant in self.plants:
            if plant.name not in unsold_flowers:
                unsold_flowers[plant.name] = len([p for p in self.plants if p.name == plant.name])
        sorted_unsold_flowers = sorted(unsold_flowers.items(), key=lambda kvp: (-kvp[1], kvp[0]))
        sorted_clients = sorted(self.clients, key=lambda c: (-c.total_orders, c.phone_number))
        orders = sum([c.total_orders for c in self.clients])
        result = (f"~Flower Shop Report~\n"
                  f"Income: {self.income:.2f}\n"
                  f"Count of orders: {orders}\n"
                  f"~~Unsold plants: {sum(unsold_flowers.values())}~~\n")

        for plant_name, count in sorted_unsold_flowers:
            result += f"{plant_name}: {count}\n"

        result += f"~~Clients number: {len(sorted_clients)}~~\n"
        result += '\n'.join([c.client_details() for c in sorted_clients])
        return result

    def filter_clients_by_phone(self, phone_number) -> list[BaseClient]:
        return [
            client
            for client in self.clients
            if client.phone_number == phone_number
        ]
