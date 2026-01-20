from dataclasses import dataclass
from datetime import date

@dataclass
class InventoryListItem:
    '''Data Transfer Object for inventory list item'''
    inventory_id: int
    person_name: str
    mobile_number: str
    date: date
