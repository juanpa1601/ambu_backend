from dataclasses import dataclass

@dataclass
class ChangeUserStatusRequest:
    '''Data Transfer Object for change user status request'''
    status: bool