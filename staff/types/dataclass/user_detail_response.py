from dataclasses import dataclass

@dataclass
class UserDetailResponse:
    '''Data Transfer Object for user detail response'''
    # System User data
    system_user_id: int
    username: str
    email: str
    first_name: str
    last_name: str
    full_name: str
    is_active: bool
    is_staff: bool
    date_joined: str
    
    # Base Staff data
    base_staff_id: int
    document_type: str
    document_number: str
    type_personnel: str
    phone_number: str | None
    address: str | None
    birth_date: str | None
    signature_url: str | None
    created_at: str
    updated_at: str
    
    # Specific profile data (depends on staff type)
    staff_type: str
    specific_data: dict | None = None