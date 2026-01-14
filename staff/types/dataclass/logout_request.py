import dataclass

@dataclass
class LogoutRequest:
    """Data Transfer Object for logout request"""
    user_id: int
    username: str
