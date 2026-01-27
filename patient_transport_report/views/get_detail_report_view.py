from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any
from rest_framework.permissions import IsAuthenticated
from core.views.base_view import BaseView
from patient_transport_report.application_service import GetDetailsReportApplicationService
from rest_framework.throttling import UserRateThrottle

class GetDetailsReportView(BaseView):
    '''
    API endpoint to retrieve complete details of a patient transport report.
    
    This is a protected endpoint that requires authentication.
    Only Healthcare and Administrative staff can access this endpoint.
    
    Returns full report with all nested relationships.
    '''
    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(
        self, 
        request: Request,
        report_id: int
    ) -> Response:
        '''
        Get complete details of a specific patient transport report.
        
        GET /api/patient-transport-report/reports/{report_id}/
        
        URL Parameters:
            report_id: Integer ID of the report to retrieve
        
        Headers:
            Authorization: Token <token_value>
        
        Permissions:
            - User must be authenticated
            - User must be Healthcare or Administrative staff
        
        Success Response (200 OK):
            {
                "response": "Report details retrieved successfully.",
                "msg": 1,
                "data": {
                    "report": {
                        "id": 1,
                        "patient": {
                            "id": 1,
                            "patient_name": "Juan Pérez",
                            "identification_type": "CC",
                            "identification_number": "1234567890",
                            "age": 45,
                            "sex": "M",
                            "phone": "3001234567",
                            "insurance_provider": 1,
                            "insurance_provider_name": "EPS Sura",
                            "affiliate_type": "contributivo",
                            "address": "Calle 123 #45-67"
                        },
                        "informed_consent": { ... },
                        "care_transfer_report": { ... },
                        "satisfaction_survey": { ... },
                        "status": "completado",
                        "created_at": "2024-01-25T10:30:00Z",
                        "updated_at": "2024-01-25T12:00:00Z",
                        "created_by": 1,
                        "created_by_username": "john_doe",
                        "updated_by": 1,
                        "updated_by_username": "john_doe"
                    }
                }
            }
        
        Error Response (401 Unauthorized):
            {
                "response": "Authentication credentials were not provided.",
                "msg": -1
            }
        
        Error Response (403 Forbidden):
            {
                "response": "Only Healthcare and Administrative staff can view report details.",
                "msg": -1
            }
        
        Error Response (404 Not Found):
            {
                "response": "Report with ID 123 not found.",
                "msg": -1
            }
        
        Error Response (500 Internal Server Error):
            {
                "response": "Error retrieving report details: <error_message>",
                "msg": -1
            }
        '''

        def service_callback(validated_data: dict | None = None) -> dict[str, Any]:
            '''
            Execute business logic to retrieve report details.
            
            Args:
                validated_data: Not used for GET requests (no input data)
            
            Returns:
                dict: Service response with complete report data
            '''
            get_details_service: GetDetailsReportApplicationService = GetDetailsReportApplicationService()
            return get_details_service.get_report_details(
                report_id=report_id,
                user=request.user
            )

        return self._handle_request(
            request=request,
            serializer_class=None,
            service_method_callback=service_callback,
            requires_auth=True
        )