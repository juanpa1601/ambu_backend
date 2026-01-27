from typing import TypedDict

class DriverResponse(TypedDict):
    '''Type definition for driver data structure'''
    id: int
    system_user_id: int
    username: str
    full_name: str
    document_type: str
    document_number: str
    is_active: bool