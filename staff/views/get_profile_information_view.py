from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.views.base_view import BaseView
from staff.application_service import GetProfileInformationApplicationService
from typing import Any
from django.contrib.auth.models import User

class GetProfileInformationView(BaseView):
    '''
    API endpoint to retrieve authenticated user's profile information.
    Requires authentication via token.
    Returns all user information excluding sensitive fields.
    
    GET /api/staff/profile/
    
    Headers:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
    
    Success Response (200 OK) - Healthcare:
        {
            "response": "Profile information retrieved successfully.",
            "msg": 1,
            "data": {
                "system_user": {
                    "id": 1,
                    "username": "healthcare_user",
                    "email": "healthcare@ambu.com",
                    "first_name": "Dr. Juan",
                    "last_name": "Pérez",
                    "full_name": "Dr. Juan Pérez",
                    "date_joined": "2026-01-15T10:30:00Z"
                },
                "base_staff": {
                    "id": 1,
                    "document_type": "DNI",
                    "document_number": "12345678",
                    "type_personnel": "Healthcare",
                    "phone_number": "+51987654321",
                    "address": "Av. Salud 123, Lima",
                    "birth_date": "1985-05-15",
                    "signature_url": "/media/signatures/signature.png",
                    "created_at": "2026-01-15T10:30:00Z",
                    "updated_at": "2026-01-16T15:45:00Z"
                },
                "staff_type": "healthcare",
                "specific_profile": {
                    "professional_registration": "CMP-12345",
                    "professional_position": "Paramedic",
                    "signature_url": "/media/signatures/healthcare/signature.png"
                }
            }
        }
    
    Success Response (200 OK) - Driver:
        {
            "response": "Profile information retrieved successfully.",
            "msg": 1,
            "data": {
                "system_user": {
                    "id": 3,
                    "username": "driver_user",
                    "email": "driver@ambu.com",
                    "first_name": "Carlos",
                    "last_name": "Rodríguez",
                    "full_name": "Carlos Rodríguez",
                    "date_joined": "2026-01-15T10:30:00Z"
                },
                "base_staff": {
                    "id": 3,
                    "document_type": "DNI",
                    "document_number": "11223344",
                    "type_personnel": "Driver",
                    "phone_number": "+51998877665",
                    "address": "Av. Transport 456, Lima",
                    "birth_date": "1990-08-20",
                    "signature_url": "/media/signatures/driver_signature.png",
                    "created_at": "2026-01-15T10:30:00Z",
                    "updated_at": "2026-01-16T15:45:00Z"
                },
                "staff_type": "driver",
                "specific_profile": {
                    "license_number": "L-2024-12345",
                    "license_category": "A-IIb",
                    "license_issue_date": "2020-01-15",
                    "license_expiry_date": "2030-01-15",
                    "blood_type": "O+"
                }
            }
        }
    
    Success Response (200 OK) - Administrative:
        {
            "response": "Profile information retrieved successfully.",
            "msg": 1,
            "data": {
                "system_user": {
                    "id": 2,
                    "username": "admin_user",
                    "email": "admin@ambu.com",
                    "first_name": "María",
                    "last_name": "González",
                    "full_name": "María González",
                    "date_joined": "2026-01-15T10:30:00Z"
                },
                "base_staff": {
                    "id": 2,
                    "document_type": "DNI",
                    "document_number": "55667788",
                    "type_personnel": "Administrative",
                    "phone_number": "+51987123456",
                    "address": "Av. Admin 789, Lima",
                    "birth_date": "1988-03-10",
                    "signature_url": "/media/signatures/admin_signature.png",
                    "created_at": "2026-01-15T10:30:00Z",
                    "updated_at": "2026-01-16T15:45:00Z"
                },
                "staff_type": "administrative",
                "specific_profile": {
                    "department": "Operations",
                    "role": "Dispatcher",
                    "access_level": "Level 2",
                    "signature_url": "/media/signatures/administrative/admin_sig.png"
                }
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
    
    def get(
        self, 
        request: Request
    ) -> Response:
        '''
        Handle GET request to retrieve authenticated user's profile information.
        Uses the token to identify the user.
        
        Args:
            request: HTTP request with authentication token
            
        Returns:
            Response with profile information or error message
        '''
        def service_callback(user: User) -> dict[str, Any]:
            get_profile_service: GetProfileInformationApplicationService = GetProfileInformationApplicationService()
            return get_profile_service.get_profile_information(user)
        
        return self._handle_request(
            request=request,
            serializer_class=None,
            service_method_callback=service_callback,
            requires_auth=True
        )