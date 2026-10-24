import unittest

from processing.preprocessing import description_or_default, is_expensive, needs_warm_clothes


class RulesTest(unittest.TestCase):
    def test_warm_clothes(self):
        self.assertTrue(needs_warm_clothes(-3.2))
        self.assertFalse(needs_warm_clothes(0))
        self.assertFalse(needs_warm_clothes(15))

    def test_expensive(self):
        self.assertTrue(is_expensive(100.5))
        self.assertFalse(is_expensive(100))
        self.assertFalse(is_expensive(92.15))

    def test_description_default(self):
        self.assertEqual(description_or_default(""), "нет данных")
        self.assertEqual(description_or_default("clear sky"), "clear sky")


if __name__ == "__main__":
    unittest.main()