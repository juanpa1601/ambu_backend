from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.views.base_view import BaseView
from staff.application_service.get_detail_user_application_service import GetDetailUserApplicationService
from typing import Any
from django.contrib.auth.models import User

class GetDetailUserView(BaseView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(
        self, 
        request: Request, 
        system_user_id: int
    ) -> Response:

        '''
        API endpoint to retrieve detailed information of a specific user.
        Requires authentication.
        
        GET /api/staff/{system_user_id}/get_detail_user/
        
        Headers:
            Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        
        Path Parameters:
            system_user_id (int): ID of the SystemUser record
        
        Success Response (200 OK):
            {
                "response": "User detail retrieved successfully.",
                "msg": 1,
                "data": {
                    "system_user": {
                        "id": 1,
                        "username": "healthcare_user",
                        "email": "healthcare@ambu.com",
                        "first_name": "Dr. Juan",
                        "last_name": "Pérez",
                        "full_name": "Dr. Juan Pérez",
                        "is_active": true,
                        "is_staff": false,
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
        
        Error Response (404 Not Found):
            {
                "response": "User not found.",
                "msg": -1
            }
        
        Error Response (401 Unauthorized):
            {
                "detail": "Authentication credentials were not provided."
            }
        '''
        def service_callback(user: User) -> dict[str, Any]:
            get_detail_user_application_service: GetDetailUserApplicationService = GetDetailUserApplicationService()
            return get_detail_user_application_service.get_user_detail(
                system_user_id=system_user_id,
                requesting_user=user
            )
        
        return self._handle_request(
            request=request,
            serializer_class=None,
            service_method_callback=service_callback,
            requires_auth=True
        )
    