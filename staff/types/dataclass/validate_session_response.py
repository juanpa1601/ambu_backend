from dataclasses import (
    dataclass,
    asdict
)
from typing import Any

@dataclass
class ValidateSessionResponse:
    '''Data Transfer Object for validate session response'''
    response: str
    msg: int
    status_code_http: int
    is_valid: bool
    username: str
    user_id: int
    staff_type: str | None

    def to_dict(self) -> dict[str, Any]:
        '''Convert dataclass to dictionary.'''
        return asdict(self)    