from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.views.base_view import BaseView
from staff.application_service import EditUserApplicationService
from staff.serializers.input import EditProfileSerializer
from staff.types.dataclass import EditProfileRequest
from typing import Any
from django.contrib.auth.models import User

class EditUserView(BaseView):
    '''
    API endpoint for administrative users to edit other user profiles.
    Requires authentication and administrative or superuser role.
    Supports updating Healthcare, Driver, or Administrative user profiles.
    
    PUT /api/staff/{system_user_id}/edit_user/
    
    Headers:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        Content-Type: application/json
    
    Path Parameters:
        system_user_id (int): ID of the user to edit
    
    Request Body - Healthcare (all fields optional):
        {
            "email": "updated.healthcare@ambu.com",
            "first_name": "Dr. Updated",
            "last_name": "Healthcare User",
            "phone_number": "+51987654399",
            "address": "Updated Address 123, Lima",
            "professional_registration": "CMP-UPDATED",
            "professional_position": "Senior Emergency Doctor"
        }
    
    Request Body - Driver (all fields optional):
        {
            "phone_number": "+51998877699",
            "license_expiry_date": "2035-01-15",
            "blood_type": "O+",
            "license_number": "L-2026-UPDATED"
        }
    
    Request Body - Administrative (all fields optional):
        {
            "email": "updated.admin@ambu.com",
            "department": "Executive Management",
            "role": "Senior Manager",
            "access_level": "Level 4"
        }
    
    Request Body - Reset Password:
        {
            "password": "NewPassword123!"
        }
    
    Success Response (200 OK):
        {
            "response": "User profile updated successfully.",
            "msg": 1,
            "data": {
                "system_user_id": 5,
                "username": "healthcare_user_2",
                "email": "updated.healthcare@ambu.com",
                "base_staff_id": 5,
                "staff_type": "healthcare",
                "updated_at": "2026-01-18T16:30:00Z",
                "fields_updated": ["email", "first_name", "last_name", "phone_number", "address", "professional_registration", "professional_position"]
            }
        }
    
    Error Response (403 Forbidden - Non-admin user):
        {
            "response": "You do not have permission to edit users.",
            "msg": -1
        }
    
    Error Response (400 Bad Request - Editing own profile):
        {
            "response": "Use the edit_profile endpoint to edit your own profile.",
            "msg": -1
        }
    
    Error Response (404 Not Found):
        {
            "response": "User not found.",
            "msg": -1
        }
    
    Error Response (400 Bad Request - Email exists):
        {
            "response": "Email already exists.",
            "msg": -1
        }
    
    Error Response (400 Bad Request - No fields):
        {
            "response": "Invalid data provided.",
            "msg": -1,
            "errors": {
                "non_field_errors": ["At least one field must be provided for update."]
            }
        }
    '''
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(
        self, 
        request: Request,
        system_user_id: int
    ) -> Response:
        '''
        Handle PUT request to edit any user's profile by admin.
        
        Args:
            request: HTTP request with authentication token and profile data
            system_user_id: ID of the user to edit
            
        Returns:
            Response with updated user profile data or error message
        '''
        def service_callback(
            validated_data: dict[str, Any], 
            user: User
        ) -> dict[str, Any]:
            # Create request dataclass
            profile_request: EditProfileRequest = EditProfileRequest(
                email=validated_data.get('email'),
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                password=validated_data.get('password'),
                phone_number=validated_data.get('phone_number'),
                address=validated_data.get('address'),
                birth_date=validated_data.get('birth_date'),
                signature=validated_data.get('signature'),
                professional_registration=validated_data.get('professional_registration'),
                professional_position=validated_data.get('professional_position'),
                license_number=validated_data.get('license_number'),
                license_category=validated_data.get('license_category'),
                license_issue_date=validated_data.get('license_issue_date'),
                license_expiry_date=validated_data.get('license_expiry_date'),
                blood_type=validated_data.get('blood_type'),
                department=validated_data.get('department'),
                role=validated_data.get('role'),
                access_level=validated_data.get('access_level')
            )
            # Call application service
            edit_user_service: EditUserApplicationService = EditUserApplicationService()
            return edit_user_service.edit_user(
                system_user_id=system_user_id,
                profile_request=profile_request,
                requesting_user=user
            )
        
        return self._handle_request(
            request=request,
            serializer_class=EditProfileSerializer,
            service_method_callback=service_callback,
            requires_auth=True
        )