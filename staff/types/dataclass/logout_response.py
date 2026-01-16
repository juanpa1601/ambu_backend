from dataclasses import dataclass

@dataclass
class LogoutResponse:
    """Data Transfer Object for logout response"""
    success: bool
    message: str