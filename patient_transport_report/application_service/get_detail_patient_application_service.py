from typing import Any
from django.contrib.auth.models import User
from patient_transport_report.models import Patient
from patient_transport_report.serializers.out import PatientDetailSerializer
from staff.models import Healthcare, Administrative
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)

class GetDetailPatientApplicationService:
    '''
    Application service for retrieving patient details by identification number.
    
    Business logic:
    - Verify user is Healthcare or Administrative staff
    - Retrieve patient with complete history and insurance data
    - Return full serialized patient data
    '''
    
    SUCCESS: int = 1
    FAILURE: int = -1

    def get_patient_details(
        self,
        identification_number: str,
        user: User
    ) -> dict[str, Any]:
        '''
        Get complete details of a patient by identification number.
        
        Args:
            identification_number: Patient's identification number (CC, TI, etc.)
            user: Authenticated user making the request
        
        Returns:
            dict: {
                'response': Success/error message
                'msg': 1 for success, -1 for error
                'status_code_http': HTTP status code
                'patient': Complete serialized patient data (if found)
            }
        
        Raises:
            Patient.DoesNotExist: If patient not found
        '''
        try:
            # Verify user has permission (Healthcare or Administrative)
            is_healthcare: bool = Healthcare.objects.filter(
                base_staff__system_user=user
            ).exists()
            is_administrative: bool = Administrative.objects.filter(
                base_staff__system_user=user
            ).exists()
            if not (is_healthcare or is_administrative):
                return {
                    'response': 'Solamente el personal de salud o administrativo puede acceder a este recurso.',
                    'msg': self.FAILURE,
                    'status_code_http': HTTP_403_FORBIDDEN
                }
            # Retrieve patient with all related data
            patient: Patient = Patient.objects.select_related(
                'patient_history',
                'insurance_provider',
                'created_by',
                'updated_by'
            ).get(
                identification_number=identification_number,
                is_deleted=False  # Only active patients
            )
            # Serialize complete patient data
            serializer: PatientDetailSerializer = PatientDetailSerializer(patient)
            return {
                'response': f'Paciente {patient.patient_name} encontrado exitosamente.',
                'msg': self.SUCCESS,
                'status_code_http': HTTP_200_OK,
                'patient': serializer.data
            }
        except Patient.DoesNotExist:
            return {
                'response': f'No se encontró ningún paciente con número de identificación {identification_number}.',
                'msg': self.FAILURE,
                'status_code_http': HTTP_404_NOT_FOUND
            }
        except Exception as e:
            return {
                'response': f'Error al recuperar los detalles del paciente: {str(e)}.',
                'msg': self.FAILURE,
                'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
            }