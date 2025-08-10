from project.gallery import Gallery

from unittest import TestCase, main

class TestGallery(TestCase):
    def test_init_with_defaults(self):
        gallery = Gallery("Ferdi", "Paris", 1.2)
        self.assertEqual("Ferdi", gallery.gallery_name)
        self.assertEqual("Paris", gallery.city)
        self.assertEqual(1.2, gallery.area_sq_m)
        self.assertTrue(gallery.open_to_public)
        self.assertDictEqual({}, gallery.exhibitions)

    def test_init_with_custom(self):
        gallery = Gallery("Ferdi", "Paris", 1.2, False)
        self.assertEqual("Ferdi", gallery.gallery_name)
        self.assertEqual("Paris", gallery.city)
        self.assertEqual(1.2, gallery.area_sq_m)
        self.assertFalse(False, gallery.open_to_public)
        self.assertDictEqual({}, gallery.exhibitions)

    def test_gallery_name_invalid_raises_exception(self):
        with self.assertRaises(ValueError) as e:
            Gallery("123 f#", "Paris", 1.2)
        self.assertEqual("Gallery name can contain letters and digits only!", str(e.exception))

    def test_city_invalid_raises_exception(self):
        with self.assertRaises(ValueError) as e:
            Gallery("Ferdi", "1Paris", 1.2)
        self.assertEqual("City name must start with a letter!", str(e.exception))

    def test_area_sq_m_invalid_raises_exception(self):
        with self.assertRaises(ValueError) as e:
            Gallery("Ferdi", "Paris", -1.2)
        self.assertEqual("Gallery area must be a positive number!", str(e.exception))

    def test_add_exhibition_invalid_raises_exception(self):
        g = Gallery("Ferdi", "Paris", 1.2)
        g.add_exhibition("Exhibition", 1)
        result = g.add_exhibition("Exhibition", 2)

        self.assertEqual('Exhibition "Exhibition" already exists.', str(result))
        self.assertEqual(1, g.exhibitions["Exhibition"])

    def test_add_exhibition_with_valid(self):
        g = Gallery("Ferdi", "Paris", 1.2)
        result = g.add_exhibition("Exhibition", 1)
        self.assertEqual('Exhibition "Exhibition" added for the year 1.', str(result))

    def test_remove_exhibition_invalid_raises_exception(self):
        g = Gallery("Ferdi", "Paris", 1.2)
        g.add_exhibition("Exhibition", 1)

        result = g.remove_exhibition("Exhibition")
        self.assertEqual('Exhibition "Exhibition" removed.', str(result))
        self.assertNotIn("Exhibition", g.exhibitions)

    def test_remove_non_existing_exhibition(self):
        g = Gallery("Ferdi", "Paris", 1.2)
        result = g.remove_exhibition("Exhibition")
        self.assertEqual('Exhibition "Exhibition" not found.', result)
        self.assertEqual({}, g.exhibitions)

    def test_list_exhibitions_open(self):
        g = Gallery("Ferdi", "Paris", 1.2, True)
        g.add_exhibition("Ferdi", 1992)
        result = g.list_exhibitions()

        self.assertEqual("Ferdi: 1992", result)

    def test_list_exhibitions_close(self):
        g = Gallery("Ferdi", "Paris", 1.2, False)
        g.add_exhibition("Ferdi", 1992)
        result = g.list_exhibitions()

        self.assertEqual(result, f'Gallery {g.gallery_name} is currently closed for public! '
                                 f'Check for updates later on.'
)


if __name__ == '__main__':
    main()