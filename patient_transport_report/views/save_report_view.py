from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any
from rest_framework.permissions import IsAuthenticated
from core.views.base_view import BaseView
from patient_transport_report.application_service import SaveReportApplicationService
from patient_transport_report.serializers.input import SaveReportInputSerializer
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth.models import User

class SaveReportView(BaseView):
    '''
    API endpoint to create or update patient transport reports.
    
    This is a protected endpoint that requires authentication.
    Supports progressive/partial completion of reports.
    
    POST /patient_transport_report/reports_save/
    
    Headers:
        Authorization: Token <token_value>
        Content-Type: application/json
    
    Request Body (CREATE - Minimum):
        {
            "report_id": null,
            "patient": {
                "patient_name": "Juan Pérez",
                "identification_type": "CC",
                "identification_number": "1234567890"
            },
            "care_transfer_report": {
                "attending_staff": 8
            }
        }
    
    Request Body (UPDATE - Add Section):
        {
            "report_id": 1,
            "informed_consent": {
                "attending_staff": 8,
                "consent_timestamp": "2024-01-26T10:00:00Z",
                "guardian_name": "María González",
                ...
            }
        }
    
    Request Body (COMPLETE):
        {
            "report_id": 1,
            "satisfaction_survey": { ... },
            "change_status_to": "completado"
        }
    
    Success Response (200 OK):
        {
            "response": "Reporte creado exitosamente.",
            "msg": 1,
            "data": {
                "report": {
                    "report_id": 1,
                    "status": "borrador",
                    "completion_percentage": 25,
                    "can_complete": false,
                    "has_patient_info": true,
                    "has_informed_consent": false,
                    "has_care_transfer": false,
                    "has_satisfaction_survey": false,
                    "sections_updated": ["patient", "care_transfer_report"]
                }
            }
        }
    
    Error Response (400 Bad Request):
        {
            "response": "Validation error",
            "msg": -1,
            "errors": {
                "attending_staff": "Healthcare staff with ID 999 not found"
            }
        }
    
    Error Response (404 Not Found):
        {
            "response": "Report with ID 123 not found",
            "msg": -1
        }
    
    Error Response (401 Unauthorized):
        {
            "detail": "Authentication credentials were not provided."
        }
    '''
    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(
        self, 
        request: Request
    ) -> Response:
        '''
        Create new report or update existing one.
        
        Supports:
        - CREATE: report_id = null + patient + attending_staff required
        - UPDATE: report_id = <int> + any section(s) to update
        - COMPLETE: change_status_to = "completado" (validates required fields)
        
        All sections are optional except:
        - patient (on CREATE)
        - attending_staff (always when care_transfer_report is sent)
        '''

        def service_callback(
            validated_data: dict, 
            user: User
        ) -> dict[str, Any]:
            '''
            Execute business logic to save/update report.
            
            Args:
                validated_data: Validated and serialized request data
            
            Returns:
                dict: Service response with report data
            '''
            save_report_service: SaveReportApplicationService = SaveReportApplicationService()
            return save_report_service.save_report(
                data=validated_data,
                user=user
            )

        return self._handle_request(
            request=request,
            serializer_class=SaveReportInputSerializer,
            service_method_callback=service_callback,
            requires_auth=True
        )