from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any
from rest_framework.permissions import IsAuthenticated
from core.views.base_view import BaseView
from patient_transport_report.application_service import ListSkinConditionApplicationService
from rest_framework.throttling import UserRateThrottle

class ListSkinConditionView(BaseView):
    '''
    API endpoint to list all skin conditions.
    
    This is a protected endpoint that requires authentication.
    Used for populating skin condition checkboxes/selects in forms.
    
    Returns all skin conditions ordered by display order.
    '''
    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(
        self, 
        request: Request
    ) -> Response:
        '''
        List all skin conditions.
        
        GET /api/patient-transport-report/skin-conditions/
        
        Headers:
            Authorization: Token <token_value>
        
        Success Response (200 OK):
            {
                "response": "Condiciones de piel recuperadas exitosamente.",
                "msg": 1,
                "data": {
                    "skin_conditions": [
                        {
                            "id": 1,
                            "name": "Pálida",
                            "order": 1
                        },
                        {
                            "id": 2,
                            "name": "Rosada",
                            "order": 2
                        },
                        {
                            "id": 3,
                            "name": "Cianótica",
                            "order": 3
                        },
                        {
                            "id": 4,
                            "name": "Ictérica",
                            "order": 4
                        },
                        {
                            "id": 5,
                            "name": "Diaforética",
                            "order": 5
                        }
                    ],
                    "total": 5
                }
            }
        
        Error Response (401 Unauthorized):
            {
                "response": "Authentication credentials were not provided.",
                "msg": -1
            }
        
        Error Response (500 Internal Server Error):
            {
                "response": "Error al recuperar condiciones de piel: <error_message>",
                "msg": -1
            }
        '''

        def service_callback(validated_data: dict | None = None) -> dict[str, Any]:
            '''
            Execute business logic to list skin conditions.
            
            Args:
                validated_data: Not used for GET requests (no input data)
            
            Returns:
                dict: Service response with skin conditions data
            '''
            list_service: ListSkinConditionApplicationService = ListSkinConditionApplicationService()
            return list_service.list_skin_conditions()

        return self._handle_request(
            request=request,
            serializer_class=None,
            service_method_callback=service_callback,
            requires_auth=True
        )