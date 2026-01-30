from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any
from rest_framework.permissions import IsAuthenticated
from core.views.base_view import BaseView
from patient_transport_report.application_service import ListHemodynamicStatusApplicationService
from rest_framework.throttling import UserRateThrottle

class ListHemodynamicStatusView(BaseView):
    '''
    API endpoint to list all hemodynamic statuses.
    
    This is a protected endpoint that requires authentication.
    Used for populating hemodynamic status checkboxes/selects in forms.
    
    Returns all hemodynamic statuses ordered by display order.
    '''
    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(
        self, 
        request: Request
    ) -> Response:
        '''
        List all hemodynamic statuses.
        
        GET /api/patient-transport-report/hemodynamic-statuses/
        
        Headers:
            Authorization: Token <token_value>
        
        Success Response (200 OK):
            {
                "response": "Estados hemodinámicos recuperados exitosamente.",
                "msg": 1,
                "data": {
                    "hemodynamic_statuses": [
                        {
                            "id": 1,
                            "name": "Estable",
                            "order": 1
                        },
                        {
                            "id": 2,
                            "name": "Inestable",
                            "order": 2
                        },
                        {
                            "id": 3,
                            "name": "Crítico",
                            "order": 3
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
                "response": "Error al recuperar estados hemodinámicos: <error_message>",
                "msg": -1
            }
        '''

        def service_callback(validated_data: dict | None = None) -> dict[str, Any]:
            '''
            Execute business logic to list hemodynamic statuses.
            
            Args:
                validated_data: Not used for GET requests (no input data)
            
            Returns:
                dict: Service response with hemodynamic statuses data
            '''
            list_service: ListHemodynamicStatusApplicationService = ListHemodynamicStatusApplicationService()
            return list_service.list_hemodynamic_statuses()

        return self._handle_request(
            request=request,
            serializer_class=None,
            service_method_callback=service_callback,
            requires_auth=True
        )