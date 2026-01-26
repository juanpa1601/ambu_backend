from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any
from rest_framework.permissions import IsAuthenticated
from core.views.base_view import BaseView
from patient_transport_report.application_service import ListIPSApplicationService
from rest_framework.throttling import UserRateThrottle

class ListIPSView(BaseView):
    '''
    API endpoint to list all active receiving institutions (IPS).
    
    This is a protected endpoint that requires authentication.
    Used for populating IPS dropdowns in forms.
    
    Returns only institutions with is_active=True.
    '''
    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(
        self, 
        request: Request
    ) -> Response:
        '''
        List all active receiving institutions (IPS).
        
        GET /api/patient-transport-report/institutions/
        
        Headers:
            Authorization: Token <token_value>
        
        Success Response (200 OK):
            {
                "response": "Institutions retrieved successfully.",
                "msg": 1,
                "data": {
                    "institutions": [
                        {
                            "id": 1,
                            "name": "Hospital Universitario San Vicente Fundación",
                            "is_active": true
                        },
                        {
                            "id": 2,
                            "name": "Clínica Las Américas",
                            "is_active": true
                        },
                        {
                            "id": 3,
                            "name": "Hospital General de Medellín",
                            "is_active": true
                        }
                    ],
                    "total": 3
                }
            }
        
        Error Response (401 Unauthorized):
            {
                "response": "Authentication credentials were not provided.",
                "msg": -1
            }
        
        Error Response (500 Internal Server Error):
            {
                "response": "Error retrieving institutions: <error_message>",
                "msg": -1
            }
        '''

        def service_callback(validated_data: dict | None = None) -> dict[str, Any]:
            '''
            Execute business logic to list active institutions.
            
            Args:
                validated_data: Not used for GET requests (no input data)
            
            Returns:
                dict: Service response with institutions data
            '''
            list_ips_service: ListIPSApplicationService = ListIPSApplicationService()
            return list_ips_service.list_active_ips()

        return self._handle_request(
            request=request,
            serializer_class=None,
            service_method_callback=service_callback,
            requires_auth=True
        )