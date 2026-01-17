from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from typing import Any
from core.views.base_view import BaseView
from staff.serializers.input import ChangeUserStatusSerializer
from staff.application_service import ChangeUserStatusApplicationService
from staff.types.dataclass import ChangeUserStatusRequest

class ChangeUserStatusView(BaseView):
    '''
    API endpoint to change user active status.
    Restricted to administrative users only.
    Cannot change status of superuser accounts.
    
    PUT /api/staff/{base_staff_id}/change_status/
    
    Headers:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        Content-Type: application/json
    
    Path Parameters:
        base_staff_id (int): ID of the BaseStaff record
    
    Request Body:
        {
            "status": true  // or false
        }
    
    Success Response (200 OK):
        {
            "response": "User successfully activated.",
            "msg": 1,
            "data": {
                "user_id": 1,
                "username": "healthcare_user",
                "new_status": true
            }
        }
    
    Error Response (403 Forbidden - Not Administrative):
        {
            "response": "You do not have permission to change user status.",
            "msg": -1
        }
    
    Error Response (400 Bad Request - Superuser):
        {
            "response": "Cannot change status of superuser accounts.",
            "msg": -1
        }
    
    Error Response (400 Bad Request - Same Status):
        {
            "response": "User is already active.",
            "msg": -1
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
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(
        self, 
        request: Request, 
        system_user_id: int
    ) -> Response:
        '''
        Handle PUT request to change user active status.
        Only administrative users can access this endpoint.
        
        Args:
            request: HTTP request with authentication token and status data
            system_user_id: ID of the SystemUser record from URL path
            
        Returns:
            Response with success message or error
        '''
        def service_callback(validated_data: dict[str, Any], user) -> dict[str, Any]:
            status_request: ChangeUserStatusRequest = ChangeUserStatusRequest(
                status=validated_data['status']
            )
            change_status_service: ChangeUserStatusApplicationService = ChangeUserStatusApplicationService()
            return change_status_service.change_user_status(
                system_user_id=system_user_id,
                status_request=status_request,
                requesting_user=user
            )
        
        return self._handle_request(
            request=request,
            serializer_class=ChangeUserStatusSerializer,
            service_method_callback=service_callback,
            requires_auth=True
        )