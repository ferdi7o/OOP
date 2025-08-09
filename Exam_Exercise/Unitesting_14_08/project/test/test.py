from project.furniture import Furniture

from unittest import TestCase, main

class TestFurnuture(TestCase):
    def test_init_with_defaults(self):
        furniture = Furniture("Ferdi", 10, (1,2,3))
        self.assertEqual(furniture.model, "Ferdi")
        self.assertEqual(furniture.price, 10)
        self.assertEqual(furniture.dimensions, (1,2,3))
        self.assertTrue(furniture.in_stock)
        self.assertIsNone(furniture.weight)

    def test_init_pass_for_defaults(self):
        furniture = Furniture("Ferdi", 10, (1, 2, 3), False, 1 )
        self.assertEqual(furniture.model, "Ferdi")
        self.assertEqual(furniture.price, 10)
        self.assertEqual(furniture.dimensions, (1, 2, 3))
        self.assertFalse(furniture.in_stock, False)
        self.assertEqual(furniture.weight, 1)

    def test_model_invalid_raises_error(self):
        with self.assertRaises(ValueError) as e:
            Furniture("  ", 10, (1, 2, 3))
        self.assertEqual("Model must be a non-empty string with a maximum length of 50 characters.", str(e.exception))

        with self.assertRaises(ValueError) as e:
            Furniture("F "*51, 10, (1, 2, 3))
        self.assertEqual("Model must be a non-empty string with a maximum length of 50 characters.", str(e.exception))

    def test_negative_price(self):
        with self.assertRaises(ValueError) as e:
            Furniture("Ferdi", -1, (1, 2, 3))
        self.assertEqual("Price must be a non-negative number.", str(e.exception))

    def test_dimensions_chars_with_than_three(self):
        with self.assertRaises(ValueError) as e:
            Furniture("ferdi", 10, (1, 2))
        self.assertEqual("Dimensions tuple must contain 3 integers.", str(e.exception))

        with self.assertRaises(ValueError) as e:
            Furniture("ferdi", 10, (1, 2, 3, 4))
        self.assertEqual("Dimensions tuple must contain 3 integers.", str(e.exception))

    def test_negative_dimensions(self):
        with self.assertRaises(ValueError) as e:
            Furniture("Ferdi", 10, (1, 2, -3))
        self.assertEqual("Dimensions tuple must contain integers greater than zero.", str(e.exception))

    def test_negative_weights(self):
        with self.assertRaises(ValueError) as e:
            Furniture("Ferdi", 10, (1, 2, 3), False, -1 )
        self.assertEqual("Weight must be greater than zero.", str(e.exception))

    def test_get_available_status(self):
        f = Furniture("Ferdi", 10, (1, 2, 3), True, 1 )
        result = f.get_available_status()
        self.assertEqual(result, f"Model: {f.model} is currently in stock.")

    def test_get_unavailable_status(self):
        f = Furniture("Ferdi", 10, (1, 2, 3), False, 1 )
        result = f.get_available_status()
        self.assertEqual(result, f"Model: {f.model} is currently unavailable.")

    def test_get_specifications_no_weight(self):
        f = Furniture("Ferdi", 10, (1, 2, 3), False)
        result = f.get_specifications()
        self.assertEqual(result, f"Model: {f.model} has the following dimensions: "
                                 f"1mm x 2mm x 3mm and weighs: N/A" )

    def test_get_specifications_with_weight(self):
        f = Furniture("Ferdi", 10, (1, 2, 3), True, 1 )
        result = f.get_specifications()
        self.assertEqual(result, f"Model: {f.model} has the following dimensions: "
                                 f"1mm x 2mm x 3mm and weighs: 1" )


if __name__ == "__main__":
    main()