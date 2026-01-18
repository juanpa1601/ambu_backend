from dataclasses import dataclass

@dataclass
class CreateUserRequest:
    '''Data Transfer Object for create user request'''
    # System User fields (required)
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    
    # Base Staff fields (required)
    document_type: str
    document_number: str
    type_personnel: str  # "Healthcare", "Administrative", "Driver"
    phone_number: str
    address: str
    birth_date: str  # Format: YYYY-MM-DD
    
    # Optional fields
    signature: str | None = None  # Base64 or file path
    
    # Specific profile data (depends on type_personnel)
    # Healthcare fields
    professional_registration: str | None = None
    professional_position: str | None = None
    
    # Driver fields
    license_number: str | None = None
    license_category: str | None = None
    license_issue_date: str | None = None
    license_expiry_date: str | None = None
    blood_type: str | None = None
    
    # Administrative fields
    department: str | None = None
    role: str | None = None
    access_level: str | None = None