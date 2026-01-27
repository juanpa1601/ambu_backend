from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from typing import Any
from core.views.base_view import BaseView
from staff.application_service import ListDriversApplicationService

class ListDriversView(BaseView):
    '''
    API endpoint to list all active drivers.
    Protected endpoint - requires authentication.
    
    GET /api/staff/drivers/
    
    Headers:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
    
    Success Response (200 OK):
        {
            "response": "Drivers retrieved successfully.",
            "msg": 1,
            "status_code": 200,
            "data": {
                "drivers": [
                    {
                        "id": 1,
                        "system_user_id": 5,
                        "username": "pedro_lopez",
                        "full_name": "Pedro López",
                        "document_type": "CC",
                        "document_number": "12345678",
                        "is_active": true
                    },
                    {
                        "id": 2,
                        "system_user_id": 8,
                        "username": "maria_garcia",
                        "full_name": "María García",
                        "document_type": "CC",
                        "document_number": "87654321",
                        "is_active": true
                    }
                ],
                "total_count": 2
            }
        }
    
    Error Response (401 Unauthorized):
        {
            "detail": "Authentication credentials were not provided."
        }
    
    Error Response (500 Internal Server Error):
        {
            "response": "Error retrieving drivers: <error_message>",
            "msg": -1,
            "status_code": 500
        }
    '''
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(
        self,
        request: Request
    ) -> Response:
        '''
        Handle GET request to list all active drivers.
        Any authenticated user can access this endpoint.
        
        Args:
            request: HTTP request with authentication token
            
        Returns:
            Response with list of active drivers
        '''
        def service_callback(user: User) -> dict[str, Any]:
            list_drivers_service: ListDriversApplicationService = ListDriversApplicationService()
            return list_drivers_service.list_drivers(user)
        
        return self._handle_request(
            request=request,
            serializer_class=None,
            service_method_callback=service_callback,
            requires_auth=True
        )