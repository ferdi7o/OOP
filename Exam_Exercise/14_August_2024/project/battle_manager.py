# battle_manager.py

from project.battleships.base_battleship import BaseBattleship
from project.battleships.pirate_battleship import PirateBattleship
from project.battleships.royal_battleship import RoyalBattleship
from project.zones.base_zone import BaseZone
from project.zones.pirate_zone import PirateZone
from project.zones.royal_zone import RoyalZone


class BattleManager:
    def __init__(self):
        self.zones: list[BaseZone] = []
        self.ships: list[BaseBattleship] = []

    def add_zone(self, zone_type: str, zone_code: str):
        if zone_type not in ("RoyalZone", "PirateZone"):
            raise Exception("Invalid zone type!")

        if any(z.code == zone_code for z in self.zones):
            raise Exception("Zone already exists!")

        if zone_type == "RoyalZone":
            zone = RoyalZone(zone_code)
        else:
            zone = PirateZone(zone_code)

        self.zones.append(zone)
        return f"A zone of type {zone_type} was successfully added."

    def add_battleship(self, ship_type: str, name: str, health: int, hit_strength: int):
        if ship_type not in ("RoyalBattleship", "PirateBattleship"):
            raise Exception(f"{ship_type} is an invalid type of ship!")

        if ship_type == "RoyalBattleship":
            ship = RoyalBattleship(name, health, hit_strength)
        else:
            ship = PirateBattleship(name, health, hit_strength)

        self.ships.append(ship)
        return f"A new {ship_type} was successfully added."

    def add_ship_to_zone(self, zone: BaseZone, ship: BaseBattleship):
        if zone.volume <= 0:
            return f"Zone {zone.code} does not allow more participants!"

        if ship.health <= 0:
            return f"Ship {ship.name} is considered sunk! Participation not allowed!"

        if not ship.is_available:
            return f"Ship {ship.name} is not available and could not participate!"

        # tip uyumu kontrolü
        same_type = (
            isinstance(zone, RoyalZone) and isinstance(ship, RoyalBattleship)
        ) or (
            isinstance(zone, PirateZone) and isinstance(ship, PirateBattleship)
        )

        ship.is_attacking = same_type  # saldırgan mı? düşman mı?
        zone.ships.append(ship)
        ship.is_available = False
        zone.volume -= 1

        return f"Ship {ship.name} successfully participated in zone {zone.code}."

    def remove_battleship(self, ship_name: str):
        ship = next((s for s in self.ships if s.name == ship_name), None)

        if not ship:
            return "No ship with this name!"

        if not ship.is_available:
            return "The ship participates in zone battles! Removal is impossible!"

        self.ships.remove(ship)
        return f"Successfully removed ship {ship_name}."

    def start_battle(self, zone: BaseZone):
        attackers = [s for s in zone.ships if s.is_attacking]
        targets = [s for s in zone.ships if not s.is_attacking]

        if not attackers or not targets:
            return "Not enough participants. The battle is canceled."

        attacker = max(attackers, key=lambda s: s.hit_strength)
        target = max(targets, key=lambda s: s.health)

        attacker.attack()
        target.take_damage(attacker)

        if target.health <= 0:
            zone.ships.remove(target)
            if target in self.ships:
                self.ships.remove(target)
            return f"{target.name} lost the battle and was sunk."

        if attacker.ammunition <= 0:
            zone.ships.remove(attacker)
            if attacker in self.ships:
                self.ships.remove(attacker)
            return f"{attacker.name} ran out of ammunition and leaves."

        return "Both ships survived the battle."

    def get_statistics(self):
        available_ships = [s.name for s in self.ships if s.is_available]
        result = []

        result.append(f"Available Battleships: {len(available_ships)}")
        if available_ships:
            result.append(f"#{', '.join(available_ships)}#")

        result.append("***Zones Statistics:***")
        result.append(f"Total Zones: {len(self.zones)}")

        for zone in sorted(self.zones, key=lambda z: z.code):
            result.append(zone.zone_info())

        return "\n".join(result)
