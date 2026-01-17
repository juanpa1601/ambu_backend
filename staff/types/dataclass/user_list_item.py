from dataclasses import dataclass

@dataclass
class UserListItem:
    '''Data Transfer Object for user list item'''
    system_user_id: int
    full_name: str
    is_active: bool
    document_type: str
    document_number: str