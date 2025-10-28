import unittest
from unittest.mock import MagicMock
from datareader import ItemRepository, Item

class TestItemRepository(unittest.TestCase):
    def setUp(self):
        self.mock_data_reader = MagicMock()
        self.mock_items = [
            Item(id=1, name='Hummer', type='Tool', condition='Mint', amount=10),
            Item(id=2, name='Nails', type='Fasteners', condition='Good', amount=450),
            Item(id=3, name='Screwdriver', type='Tool', condition='Bad', amount=100)
        ]
        self.mock_data_reader.read.return_value = self.mock_items
        self.repo = ItemRepository(self.mock_data_reader)
        self.repo.load_data('dummy_path.csv')

    def test_load_data(self):
        self.mock_data_reader.read.assert_called_once_with('dummy_path.csv')
        self.assertEqual(len(self.repo._items), 3)

    def test_get_items_page(self):
        page1 = self.repo.get_items_page(1, 2)
        self.assertEqual(len(page1), 2)
        self.assertEqual(page1[0].name, 'Hummer')

        page2 = self.repo.get_items_page(2, 2)
        self.assertEqual(len(page2), 1)
        self.assertEqual(page2[0].name, 'Screwdriver')

    def test_get_item_by_id(self):
        item = self.repo.get_item_by_id(2)
        self.assertIsNotNone(item)
        self.assertEqual(item.name, 'Nails')

        item_not_found = self.repo.get_item_by_id(99)
        self.assertIsNone(item_not_found)

    def test_search_by_name(self):
        results = self.repo.search_by_name('nails')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, 2)

        results = self.repo.search_by_name('tool')
        self.assertEqual(len(results), 2)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)