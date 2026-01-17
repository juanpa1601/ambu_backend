from dataclasses import dataclass
from .user_list_item import UserListItem

@dataclass
class UserListResponse:
    '''Data Transfer Object for user list response'''
    users: list[UserListItem]
    total_count: int