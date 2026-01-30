from dataclasses import dataclass

@dataclass
class ProfileInformationResponse:
    '''Data Transfer Object for profile information response'''
    # System User data (sin campos sensibles)
    system_user_id: int
    username: str
    email: str
    first_name: str
    last_name: str
    full_name: str
    date_joined: str
    
    # Base Staff data
    base_staff_id: int
    document_type: str
    document_number: str
    type_personnel: str
    phone_number: str | None
    address: str | None
    birth_date: str | None
    created_at: str
    updated_at: str
    
    # Specific profile data
    staff_type: str
    specific_data: dict | None = None