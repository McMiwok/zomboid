import csv
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Item:
    id: int
    name: str
    type: str
    condition: str
    amount: int

class DataReader(ABC):
    @abstractmethod
    def read(self, file_path: str) -> List[Item]:
        pass

class CsvDataReader(DataReader):
    def read(self, file_path: str) -> List[Item]:
        items: List[Item] = []
        try:
            with open(file=file_path, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Convert string values to their respective types
                    items.append(Item(
                        id=int(row['ID']),
                        name=row['Name'],
                        type=row['Type'],
                        condition=row['Condition'],
                        amount=int(row['Amount'])
                    ))
        except FileNotFoundError:
            print(f"Error: File not found at path {file_path}")
            return []
        return items
    
class JsonDataReader(DataReader):
    def read(self, file_path: str) -> List[Item]:
        try:
            with open(file=file_path, encoding='utf-8') as f:
                data = json.load(f)
                items = [Item(**d) for d in data]
                return items
        except (FileNotFoundError, json.JSONDecodeError, TypeError) as e:
            print(f"Error: Reading JSON: {e}")
            return []    

class ItemRepository:
    def __init__(self, data_reader: DataReader):
        self._data_reader = data_reader
        self._items: List[Item] = []

    def load_data(self, file_path: str):
        #Loads data from the file using the provided DataReader
        self._items = self._data_reader.read(file_path)

    def get_items_page(self, page_number: int, page_size: int) -> List[Item]:
        #Returns a list of items for the specified page
        if not self._items:
            return []
        
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        
        return self._items[start_index:end_index]

    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        for item in self._items:
            if item.id == item_id:
                return item
        return None

    def search_by_name(self, name: str) -> List[Item]:
        return [item for item in self._items if name in item.name]
    
    def get_condition_percentage(self) -> Dict[str, str]:
        if not self._items:
            return {}

        total_items = len(self._items)
        condition_counts: Dict[str, int] = {}

        for item in self._items:
            condition = item.condition
            condition_counts[condition] = condition_counts.get(condition, 0) + 1

        percentages: Dict[str, str] = {}
        for condition, count in condition_counts.items():
            percentage = (count / total_items) * 100
            percentages[condition] = f"{percentage:.2f}%"

        return percentages

    def get_condition_percentage_by_name(self, name: str) -> Dict[str, str]:
        filtered_items = self.search_by_name(name)
        if not filtered_items:
            return {}

        total_filtered_items = len(filtered_items)
        condition_counts: Dict[str, int] = {}

        for item in filtered_items:
            condition = item.condition
            condition_counts[condition] = condition_counts.get(condition, 0) + 1

        percentages: Dict[str, str] = {}
        for condition, count in condition_counts.items():
            percentage = (count / total_filtered_items) * 100
            percentages[condition] = f"{percentage:.2f}%"

        return percentages