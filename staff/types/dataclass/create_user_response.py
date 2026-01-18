from dataclasses import dataclass

@dataclass
class CreateUserResponse:
    '''Data Transfer Object for create user response'''
    system_user_id: int
    username: str
    email: str
    base_staff_id: int
    staff_type: str
    created_at: str