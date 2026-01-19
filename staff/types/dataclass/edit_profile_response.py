from dataclasses import dataclass

@dataclass
class EditProfileResponse:
    '''Data Transfer Object for edit profile response'''
    system_user_id: int
    username: str
    email: str
    base_staff_id: int
    staff_type: str
    updated_at: str
    fields_updated: list[str]