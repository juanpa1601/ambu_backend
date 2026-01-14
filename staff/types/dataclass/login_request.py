from dataclasses import dataclass

@dataclass
class LoginRequest:
    '''Data Transfer Object for login request'''
    username: str
    password: str