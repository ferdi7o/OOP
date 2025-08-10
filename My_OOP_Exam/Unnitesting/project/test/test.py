from project.legendary_item import LegendaryItem

from unittest import TestCase, main
class TestLegendaryItem(TestCase):
    def test_init_with_customs(self):
        legendaries = LegendaryItem("Ferdi", 1, 5, 10)
        self.assertEqual(legendaries.identifier, "Ferdi")
        self.assertEqual(legendaries.power, 1)
        self.assertEqual(legendaries.durability, 5)
        self.assertEqual(legendaries.price, 10)

    def test_identifier_not_isalnum(self):
        with self.assertRaises(ValueError) as e:
            LegendaryItem("F@!erdi", 1, 5, 10)
        self.assertEqual("Identifier can only contain letters, digits, or hyphens!", str(e.exception))

        with self.assertRaises(ValueError) as e:
            LegendaryItem("Fer", 1, 5, 10)
        self.assertEqual("Identifier must be at least 4 characters long!", str(e.exception))

    def test_power_with_negative(self):
        with self.assertRaises(ValueError) as e:
            LegendaryItem("Ferdi", -1, 5, 10)
        self.assertEqual("Power must be a non-negative integer!", str(e.exception))

    def test_durability_from_1_to_100_ink(self):
        with self.assertRaises(ValueError) as e:
            LegendaryItem("Ferdi", 1, 111, 10)
        self.assertEqual("Durability must be between 1 and 100 inclusive!", str(e.exception))

    def test_price_with_not_acceptable(self):
        with self.assertRaises(ValueError) as e:
            LegendaryItem("Ferdi", 1, 5, 9)
        self.assertEqual("Price must be a multiple of 10 and not 0!", str(e.exception))

    def test_is_precious_with_True(self):
        result = LegendaryItem("Ferdi", 1, 5, 10)
        result.power += 100
        self.assertTrue(result.is_precious)

    def test_is_precious_with_False(self):
        result = LegendaryItem("Ferdi", 1, 5, 10)
        self.assertFalse(result.is_precious)

    def test_enhance(self):
        result = LegendaryItem("Ferdi", 1, 5, 10)
        result.enhance()

        self.assertEqual(result.power, 2)
        self.assertEqual(result.durability, 15)
        self.assertEqual(result.price, 20)

    def test_low_durability(self):
        item = LegendaryItem("Ferdi", 1, 5, 10)
        result = item.evaluate(min_durability=80)
        self.assertEqual(result, "Item not eligible.")

    def test_high_durability_with_true(self):
        item = LegendaryItem("Ferdi", 100, 85, 10)
        result = item.evaluate(min_durability=85)
        self.assertEqual(result, f"{item.identifier} is eligible.")

    def test_durability_below_range(self):
        with self.assertRaises(ValueError) as e:
            LegendaryItem("Ferdi", 1, 0, 10)
        self.assertEqual("Durability must be between 1 and 100 inclusive!", str(e.exception))

    def test_high_durability_with_false(self):
        item = LegendaryItem("Ferdi", 1, 85, 10)
        result = item.evaluate(min_durability=85)
        self.assertEqual(result, f"Item not eligible.")

    def test_enhance_durability_not_than_100(self):
        result = LegendaryItem("Ferdi", 1, 95, 10)
        result.enhance()
        self.assertEqual(result.durability, 100)

if __name__ == '__main__':
    main()
