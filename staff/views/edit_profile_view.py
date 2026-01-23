from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.views.base_view import BaseView
from staff.application_service import EditProfileApplicationService
from staff.serializers.input import EditProfileSerializer
from staff.types.dataclass import EditProfileRequest
from typing import Any
from django.contrib.auth.models import User

class EditProfileView(BaseView):
    '''
    API endpoint for authenticated users to edit their own profile.
    Requires authentication via token.
    Supports updating Healthcare, Driver, or Administrative specific fields.
    
    PUT /api/staff/edit_profile/
    
    Headers:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        Content-Type: application/json
    
    Request Body - Healthcare (all fields optional):
        {
            "email": "newemail@ambu.com",
            "first_name": "Dr. Ana Updated",
            "phone_number": "+51987654399",
            "address": "New Address 123, Lima",
            "professional_position": "Senior Doctor"
        }
    
    Request Body - Driver (all fields optional):
        {
            "phone_number": "+51998877699",
            "address": "New Driver Address, Lima",
            "license_expiry_date": "2035-01-15",
            "blood_type": "O+"
        }
    
    Request Body - Administrative (all fields optional):
        {
            "email": "updated.admin@ambu.com",
            "phone_number": "+51987123499",
            "department": "New Department",
            "role": "Senior Manager"
        }
    
    Request Body - Change Password:
        {
            "password": "NewSecurePass123!"
        }
    
    Success Response (200 OK):
        {
            "response": "Profile updated successfully.",
            "msg": 1,
            "data": {
                "system_user_id": 1,
                "username": "healthcare_user",
                "email": "newemail@ambu.com",
                "base_staff_id": 1,
                "staff_type": "healthcare",
                "updated_at": "2026-01-18T15:30:00Z",
                "fields_updated": ["email", "first_name", "phone_number", "address", "professional_position"]
            }
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
    
    Error Response (404 Not Found):
        {
            "response": "User profile not found.",
            "msg": -1
        }
    
    Error Response (401 Unauthorized):
        {
            "detail": "Authentication credentials were not provided."
        }
    '''
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(
        self, 
        request: Request
    ) -> Response:
        '''
        Handle PUT request to edit authenticated user's profile.
        
        Args:
            request: HTTP request with authentication token and profile data
            
        Returns:
            Response with updated profile data or error message
        '''
        def service_callback(
            validated_data: dict[str, Any], 
            user: User
        ) -> dict[str, Any]:
            # Create request dataclass
            profile_request: EditProfileRequest = EditProfileRequest(
                username=validated_data.get('username'),
                email=validated_data.get('email'),
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                password=validated_data.get('password'),
                document_type=validated_data.get('document_type'),
                document_number=validated_data.get('document_number'),
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
            edit_profile_service: EditProfileApplicationService = EditProfileApplicationService()
            return edit_profile_service.edit_profile(
                profile_request=profile_request,
                authenticated_user=user
            )
        
        return self._handle_request(
            request=request,
            serializer_class=EditProfileSerializer,
            service_method_callback=service_callback,
            requires_auth=True
        )