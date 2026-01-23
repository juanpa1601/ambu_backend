from dataclasses import dataclass

@dataclass
class EditProfileRequest:
    '''Data Transfer Object for edit profile request'''
    # System User fields (optional)
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None # New password
    
    # Base Staff fields (optional)
    document_type: str | None = None
    document_number: str | None = None
    phone_number: str | None = None
    address: str | None = None
    birth_date: str | None = None  # Format: YYYY-MM-DD
    signature: str | None = None  # Base64 or file path
    
    # Healthcare specific fields (optional)
    professional_registration: str | None = None
    professional_position: str | None = None
    
    # Driver specific fields (optional)
    license_number: str | None = None
    license_category: str | None = None
    license_issue_date: str | None = None
    license_expiry_date: str | None = None
    blood_type: str | None = None
    
    # Administrative specific fields (optional)
    department: str | None = None
    role: str | None = None
    access_level: str | None = None

