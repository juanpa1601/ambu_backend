from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.views.base_view import BaseView
from staff.application_service import ValidateSessionApplicationService
from typing import Any
from django.contrib.auth.models import User

class ValidateSessionView(BaseView):
    '''
    API endpoint to validate if authentication token is still valid.
    Requires authentication via token.
    
    GET /api/staff/validate-session/
    
    Headers:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
    
    Success Response (200 OK):
        {
            "response": "Session is valid.",
            "msg": 1,
            "data": {
                "is_valid": true,
                "user": {
                    "id": 1,
                    "username": "healthcare_user",
                    "email": "healthcare@ambu.com",
                    "full_name": "Dr. Juan Pérez",
                    "staff_type": "healthcare"
                }
            }
        }
    
    Error Response (401 Unauthorized - Invalid Token):
        {
            "detail": "Invalid token."
        }
    
    Error Response (401 Unauthorized - No Token):
        {
            "detail": "Authentication credentials were not provided."
        }
    
    Error Response (401 Unauthorized - Inactive User):
        {
            "response": "User account is inactive.",
            "msg": -1,
            "data": {
                "is_valid": false
            }
        }
    '''
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(
        self, 
        request: Request
    ) -> Response:
        '''
        Handle GET request to validate user session.
        Uses the token from headers to validate session.
        
        Args:
            request: HTTP request with authentication token
            
        Returns:
            Response indicating if session is valid
        '''
        def service_callback(user: User) -> dict[str, Any]:
            validate_session_service: ValidateSessionApplicationService = ValidateSessionApplicationService()
            return validate_session_service.validate_session(
                authenticated_user=user
            )
        
        return self._handle_request(
            request=request,
            serializer_class=None,
            service_method_callback=service_callback,
            requires_auth=True
        )