from unittest import TestCase, main

from project.vehicle import Vehicle


class TestVehicle(TestCase):
    fuel = 5.8
    horse_power = 50.0

    def setUp(self):
        self.test_vehicle = Vehicle(self.fuel, self.horse_power)

    def test_class_attributes(self):
        self.assertIsInstance(self.test_vehicle.DEFAULT_FUEL_CONSUMPTION, float)
        self.assertIsInstance(self.test_vehicle.fuel_consumption, float)
        self.assertIsInstance(self.test_vehicle.fuel, float)
        self.assertIsInstance(self.test_vehicle.capacity, float)
        self.assertIsInstance(self.test_vehicle.horse_power, float)


    def test_init(self):
        self.assertEqual(self.fuel, self.test_vehicle.fuel)
        self.assertEqual(self.fuel, self.test_vehicle.capacity)
        self.assertEqual(self.horse_power, self.test_vehicle.horse_power)
        self.assertEqual(1.25, self.test_vehicle.fuel_consumption)

    def test_drive_success(self):
        self.test_vehicle.drive(3)
        self.assertEqual(2.05, self.test_vehicle.fuel)

    def test_drive_failure(self):
        with self.assertRaises(Exception) as e:
            self.test_vehicle.drive(15)
        self.assertEqual("Not enough fuel", str(e.exception))

    def test_refuel_success(self):
        self.test_vehicle.fuel = 1
        self.test_vehicle.refuel(2.4)
        self.assertEqual(3.4, self.test_vehicle.fuel)

    def test_refuel_failure(self):
        self.test_vehicle.fuel = 50
        with self.assertRaises(Exception) as e:
            self.test_vehicle.refuel(10)
        self.assertEqual("Too much fuel", str(e.exception))

    def test_str(self):
        expected = (f"The vehicle has {self.horse_power} "
                    f"horse power with {self.fuel} fuel left"
                    f" and 1.25 fuel consumption")
        self.assertEqual(expected, self.test_vehicle.__str__())



if __name__ == '__main__':
    main()