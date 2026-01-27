from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any
from rest_framework.permissions import IsAuthenticated
from core.views.base_view import BaseView
from patient_transport_report.application_service import ListDiagnosisApplicationService
from rest_framework.throttling import UserRateThrottle

class ListDiagnosisView(BaseView):
    '''
    API endpoint to list and search available diagnoses (CIE-10 codes).
    
    This is a protected endpoint that requires authentication.
    Used for populating diagnosis dropdowns and autocomplete searches in forms.
    
    Supports search by CIE-10 code or diagnosis name (case-insensitive).
    '''
    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(
        self, 
        request: Request
    ) -> Response:
        '''
        List or search diagnosis codes (CIE-10).
        
        GET /api/patient-transport-report/diagnoses/
        GET /api/patient-transport-report/diagnoses/?q=diabetes
        GET /api/patient-transport-report/diagnoses/?q=I10
        
        Query Parameters:
            q (optional): Search query string. Minimum 2 characters.
                         Searches in both code and name fields.
        
        Headers:
            Authorization: Token <token_value>
        
        Success Response (200 OK) - Without search:
            {
                "response": "Diagnoses retrieved successfully.",
                "msg": 1,
                "data": {
                    "diagnoses": [
                        {
                            "id": 1,
                            "cie_10": "A09",
                            "cie_10_name": "Diarrea y gastroenteritis de presunto origen infeccioso",
                            "display_name": "A09 - Diarrea y gastroenteritis de presunto origen infeccioso"
                        },
                        ...
                    ],
                    "total": 150,
                    "search_applied": false,
                    "search_query": null
                }
            }
        
        Success Response (200 OK) - With search:
            {
                "response": "Diagnoses retrieved successfully.",
                "msg": 1,
                "data": {
                    "diagnoses": [
                        {
                            "id": 45,
                            "cie_10": "E11",
                            "cie_10_name": "Diabetes mellitus no insulinodependiente",
                            "display_name": "E11 - Diabetes mellitus no insulinodependiente"
                        },
                        {
                            "id": 46,
                            "cie_10": "E11.9",
                            "cie_10_name": "Diabetes mellitus no insulinodependiente sin mención de complicación",
                            "display_name": "E11.9 - Diabetes mellitus no insulinodependiente sin mención de complicación"
                        }
                    ],
                    "total": 2,
                    "search_applied": true,
                    "search_query": "diabetes"
                }
            }
        
        Error Response (401 Unauthorized):
            {
                "response": "Authentication credentials were not provided.",
                "msg": -1
            }
        
        Error Response (500 Internal Server Error):
            {
                "response": "Error retrieving diagnoses: <error_message>",
                "msg": -1
            }
        '''

        def service_callback(validated_data: dict | None = None) -> dict[str, Any]:
            '''
            Execute business logic to list or search diagnoses.
            
            Args:
                validated_data: Not used for GET requests (no input serializer)
            
            Returns:
                dict: Service response with diagnoses data
            '''
            # Get search query from URL parameters
            search_query: str | None = request.query_params.get('q', None)
            # Call application service with search parameter
            list_diagnosis_service = ListDiagnosisApplicationService()
            return list_diagnosis_service.list_diagnoses(search_query=search_query)

        return self._handle_request(
            request=request,
            serializer_class=None,  # No input serializer needed for GET
            service_method_callback=service_callback,
            requires_auth=True
        )