from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from typing import Any
from core.views.base_view import BaseView
from staff.application_service import ListUsersApplicationService

class ListUsersView(BaseView):
    '''
    API endpoint to list all staff users.
    Restricted to administrative users only.
    
    GET /api/staff/users/
    
    Headers:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
    
    Success Response (200 OK):
        {
            "response": "Users retrieved successfully.",
            "msg": 1,
            "status_code": 200,
            "data": {
                "users": [
                    {
                        "system_user_id": 1,
                        "full_name": "Dr. Juan Pérez",
                        "is_active": true,
                        "document_type": "DNI",
                        "document_number": "12345678"
                    },
                    {
                        "system_user_id": 2,
                        "full_name": "Carlos Rodríguez",
                        "is_active": true,
                        "document_type": "DNI",
                        "document_number": "11223344"
                    }
                ],
                "total_count": 2
            }
        }
    
    Error Response (403 Forbidden):
        {
            "response": "You do not have permission to access this resource.",
            "msg": -1,
            "status_code": 403
        }
    
    Error Response (401 Unauthorized):
        {
            "detail": "Authentication credentials were not provided."
        }
    '''
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request) -> Response:
        '''
        Handle GET request to list all staff users.
        Only administrative users can access this endpoint.
        
        Args:
            request: HTTP request with authentication token
            
        Returns:
            Response with list of users or permission denied
        '''
        def service_callback(user: User) -> dict[str, Any]:
            list_users_service: ListUsersApplicationService = ListUsersApplicationService()
            return list_users_service.list_users(user)
        
        return self._handle_request(
            request=request,
            serializer_class=None,
            service_method_callback=service_callback,
            requires_auth=True
        )