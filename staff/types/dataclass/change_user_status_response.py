from dataclasses import dataclass

@dataclass
class ChangeUserStatusResponse:
    '''Data Transfer Object for change user status response'''
    success: bool
    message: str
    user_id: int
    username: str
    new_status: bool