from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any
from rest_framework.permissions import AllowAny
from core.views.base_view import BaseView
from staff.serializers.input import LoginSerializer
from staff.application_service import LoginApplicationService
from staff.types.dataclass import LoginRequest

class LoginView(BaseView):
    
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(
        self, 
        request: Request
    ) -> Response:
        '''
        API endpoint for user authentication.
        
        POST /api/staff/login/
        
        Request Body:
            {
                "username": "john_doe",
                "password": "secure_password"
            }
        
        Success Response (200 OK):
            {
                "response": "Login successful.",
                "msg": 1,
                "data": {
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                    "user": {
                        "id": 1,
                        "username": "john_doe",
                        "email": "john@example.com",
                        "full_name": "John Doe",
                        "staff_type": "healthcare"
                    }
                }
            }

        
        
        Error Response (400 Bad Request):
            {
                "response": "Invalid credentials.",
                "msg": -1
            }
        '''

        def service_callback(validated_data: dict) -> dict[str, Any]:
            login_application_service: LoginApplicationService = LoginApplicationService()
            login_request: LoginRequest = LoginRequest(
                username=validated_data['username'],
                password=validated_data['password']
            )
            return login_application_service.login(login_request)

        return self._handle_request(
            request=request,
            serializer_class=LoginSerializer,
            service_method_callback=service_callback,
            requires_auth=False
        )