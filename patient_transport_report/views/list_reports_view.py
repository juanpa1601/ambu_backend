from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any
from rest_framework.permissions import IsAuthenticated
from core.views.base_view import BaseView
from patient_transport_report.application_service import ListReportsApplicationService
from rest_framework.throttling import UserRateThrottle

class ListReportsView(BaseView):
    '''
    API endpoint to list authenticated user's transport reports (inbox/buzon).
    
    This is a protected endpoint that requires authentication.
    Returns only reports created by the logged-in user within the last 48 hours.
    Reports are separated by status: draft and completed.
    '''
    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(
        self, 
        request: Request
    ) -> Response:
        '''
        List user's own transport reports from last 48 hours.
        
        GET /api/patient-transport-report/buzon/
        
        Headers:
            Authorization: Token <token_value>
        
        Filters Applied:
            - created_by: Only reports created by authenticated user
            - created_at: Only reports from last 48 hours
            - Separated by status: 'borrador' and 'completado'
        
        Success Response (200 OK):
            {
                "response": "User reports retrieved successfully.",
                "msg": 1,
                "data": {
                    "list_report_draft": [
                        {
                            "id": 1,
                            "patient_name": "Juan Pérez",
                            "patient_identification": "1234567890",
                            "status": "borrador",
                            "created_at": "2024-01-25T10:30:00Z",
                            "updated_at": "2024-01-25T11:00:00Z",
                            "created_by_username": "john_doe"
                        },
                        {
                            "id": 3,
                            "patient_name": "María García",
                            "patient_identification": "9876543210",
                            "status": "borrador",
                            "created_at": "2024-01-24T15:20:00Z",
                            "updated_at": "2024-01-24T15:20:00Z",
                            "created_by_username": "john_doe"
                        }
                    ],
                    "list_report_completed": [
                        {
                            "id": 2,
                            "patient_name": "Carlos López",
                            "patient_identification": "5555555555",
                            "status": "completado",
                            "created_at": "2024-01-25T09:00:00Z",
                            "updated_at": "2024-01-25T12:00:00Z",
                            "created_by_username": "john_doe"
                        }
                    ],
                    "total_draft": 2,
                    "total_completed": 1,
                    "filter_hours": 48
                }
            }
        
        Error Response (401 Unauthorized):
            {
                "response": "Authentication credentials were not provided.",
                "msg": -1
            }
        
        Error Response (500 Internal Server Error):
            {
                "response": "Error retrieving user reports: <error_message>",
                "msg": -1
            }
        '''

        def service_callback(validated_data: dict | None = None) -> dict[str, Any]:
            '''
            Execute business logic to list user's reports.
            
            Args:
                validated_data: Not used for GET requests (no input data)
            
            Returns:
                dict: Service response with user's reports data
            '''
            list_reports_service: ListReportsApplicationService = ListReportsApplicationService()
            return list_reports_service.list_all_reports(user=request.user)

        return self._handle_request(
            request=request,
            serializer_class=None,
            service_method_callback=service_callback,
            requires_auth=True
        )