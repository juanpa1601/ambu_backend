from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any
from rest_framework.permissions import IsAuthenticated
from core.views.base_view import BaseView
from patient_transport_report.application_service import GetDetailPatientApplicationService
from rest_framework.throttling import UserRateThrottle

class GetDetailPatientView(BaseView):
    '''
    API endpoint to retrieve complete patient details by identification number.
    
    This is a protected endpoint that requires authentication.
    Only Healthcare and Administrative staff can access this endpoint.
    
    Returns patient data including medical history and insurance provider.
    '''
    
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(
        self, 
        request: Request,
        identification_number: str
    ) -> Response:
        '''
        Retrieve complete patient details by identification number.
        
        GET /api/patient-transport-report/patients/<identification_number>/
        
        Headers:
            Authorization: Token <token_value>
        
        Path Parameters:
            identification_number (str): Patient's identification number
        
        Success Response (200 OK):
            {
                "response": "Paciente Juan Pérez encontrado exitosamente.",
                "msg": 1,
                "patient": {
                    "id": 1,
                    "patient_name": "Juan Pérez",
                    "identification_type": "CC",
                    "other_identification_type": "",
                    "identification_number": "1234567890",
                    "issue_date": "2020-01-15",
                    "issue_place": "Medellín",
                    "birth_date": "1990-05-20",
                    "patient_age": 35,
                    "sex": "M",
                    "home_address": "Calle 123 #45-67",
                    "residence_city": "Medellín",
                    "cell_phone": "+573001234567",
                    "landline_phone": "",
                    "marital_status": "Soltero",
                    "occupation": "Ingeniero",
                    "patient_history": {
                        "id": 1,
                        "has_pathology": true,
                        "pathology": "Diabetes",
                        "has_allergies": false,
                        "allergies": "",
                        "has_surgeries": true,
                        "surgeries": "Apendicectomía",
                        "has_medicines": true,
                        "medicines": "Metformina",
                        "tobacco_use": false,
                        "substance_use": false,
                        "alcohol_use": true,
                        "other_history": "Antecedentes familiares de diabetes"
                    },
                    "insurance_provider": {
                        "id": 1,
                        "coverage_type": "EPS",
                        "provider_name": "Sura",
                        "other_coverage_type": false,
                        "other_coverage_details": ""
                    },
                    "created_at": "2024-01-20T10:00:00Z",
                    "updated_at": "2024-01-25T15:30:00Z"
                }
            }
        
        Error Response (401 Unauthorized):
            {
                "response": "Authentication credentials were not provided.",
                "msg": -1
            }
        
        Error Response (403 Forbidden):
            {
                "response": "Solamente el personal de salud o administrativo puede acceder a este recurso.",
                "msg": -1
            }
        
        Error Response (404 Not Found):
            {
                "response": "No se encontró ningún paciente con número de identificación 1234567890.",
                "msg": -1
            }
        
        Error Response (500 Internal Server Error):
            {
                "response": "Error al recuperar los detalles del paciente: <error_message>",
                "msg": -1
            }
        '''

        def service_callback(validated_data: dict | None = None) -> dict[str, Any]:
            '''
            Execute business logic to retrieve patient details.
            
            Args:
                validated_data: Not used for GET requests (no input data)
            
            Returns:
                dict: Service response with patient data
            '''
            get_patient_service: GetDetailPatientApplicationService = GetDetailPatientApplicationService()
            return get_patient_service.get_patient_details(
                identification_number=identification_number,
                user=request.user
            )

        return self._handle_request(
            request=request,
            serializer_class=None,
            service_method_callback=service_callback,
            requires_auth=True
        )