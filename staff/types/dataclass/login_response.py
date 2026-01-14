from dataclasses import dataclass

@dataclass
class LoginResponse:
    '''Data Transfer Object for login response'''
    access_token: str
    system_user_id: int
    username: str
    email: str
    full_name: str
    staff_type: str | None = None