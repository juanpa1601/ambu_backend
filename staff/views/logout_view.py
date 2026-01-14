from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from typing import Any
from django.contrib.auth.models import User
from core.views.base_view import BaseView
from staff.application_service import LogoutApplicationService
from staff.types.dataclass import LogoutRequest

class LogoutView(BaseView):

    authentication_classes = [TokenAuthentication]  # Protected endpoint
    permission_classes = [IsAuthenticated]  # Requires authentication
    
    def post(
        self, 
        request: Request
    ) -> Response:
        '''
        API endpoint for user logout.
        Requires authentication - deletes the user's token from database.
        
        POST /api/staff/logout/
        
        Headers:
            Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        
        Request Body:
            {} (empty - user identified by token)
        
        Success Response (200 OK):
            {
                "response": "Logout successful",
                "msg": 1,
                "data": {
                    "success": true,
                    "username": "john_doe"
                }
            }
        
        Error Response (401 Unauthorized):
            {
                "detail": "Authentication credentials were not provided."
            }
        
        Error Response (400 Bad Request):
            {
                "response": "No active session found.",
                "msg": -1
            }
        '''
        def service_callback(user: User) -> dict[str, Any]:
            logout_application_service: LogoutApplicationService = LogoutApplicationService()
            logout_request = LogoutRequest(
                user_id=user.id,
                username=user.username
            )
            return logout_application_service.logout(
                logout_request=logout_request,
                user=user
            )

        return self._handle_request(
            request=request,
            serializer_class=None,
            service_method_callback=service_callback,
            requires_auth=True
        )