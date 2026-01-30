from typing import Any
from django.contrib.auth.models import User
from ..models import PatientTransportReport
from ..serializers.out import PatientTransportReportDetailSerializer
from staff.models import (
    Healthcare, 
    Administrative
)
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)

class GetDetailsReportApplicationService:
    '''
    Application service for retrieving detailed patient transport report.
    
    Business logic:
    - Verify user is Healthcare or Administrative staff
    - Retrieve complete report with all nested relationships
    - Return full serialized data
    '''
    
    SUCCESS: int = 1
    FAILURE: int = -1       

    def get_report_details(
        self, 
        report_id: int,
        user: User
    ) -> dict[str, Any]:
        '''    
        Get complete details of a patient transport report.
        
        Args:
            report_id: ID of the report to retrieve
            user: Authenticated user making the request
        
        Returns:
            dict: {
                'response': Success/error message
                'msg': 1 for success, -1 for error
                'status_code_http': HTTP status code
                'report': Complete serialized report data
            }
        
        Raises:
            PatientTransportReport.DoesNotExist: If report not found
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
            # Retrieve report with all relationships using select_related and prefetch_related
            report: PatientTransportReport = PatientTransportReport.objects.select_related(
                
                # Attending Staff
                'attending_staff',
                'attending_staff__base_staff',
                # Patient
                'patient',
                'patient__patient_history',
                'patient__insurance_provider',
                
                # Informed Consent
                'informed_consent',
                'informed_consent__outgoing_entity',
                
                # Care Transfer Report
                'care_transfer_report',
                'care_transfer_report__driver',
                'care_transfer_report__driver__base_staff',
                'care_transfer_report__ambulance',
                'care_transfer_report__companion',
                'care_transfer_report__responsible',
                'care_transfer_report__initial_physical_exam',
                'care_transfer_report__initial_physical_exam__glasgow',
                'care_transfer_report__final_physical_exam',
                'care_transfer_report__final_physical_exam__glasgow',
                'care_transfer_report__treatment',
                'care_transfer_report__diagnosis_1',
                'care_transfer_report__diagnosis_2',
                'care_transfer_report__ips',
                'care_transfer_report__result',
                'care_transfer_report__complications_transfer',
                'care_transfer_report__receiving_entity',
                
                # Satisfaction Survey
                'satisfaction_survey',
                
                # Audit fields
                'created_by',
                'updated_by'
            ).prefetch_related(
                'informed_consent__required_procedures',
                'informed_consent__medication_administration',
                'care_transfer_report__skin_conditions',
                'care_transfer_report__hemodynamic_statuses'
            ).get(id=report_id)
            # Serialize complete report
            serializer: PatientTransportReportDetailSerializer = PatientTransportReportDetailSerializer(report)
            return {
                'response': 'Detalles del informe recuperados con éxito.',
                'msg': self.SUCCESS,
                'status_code_http': HTTP_200_OK,
                'report': serializer.data
            }
        except PatientTransportReport.DoesNotExist:
            return {
                'response': f'Informe con ID {report_id} no encontrado.',
                'msg': self.FAILURE,
                'status_code_http': HTTP_404_NOT_FOUND
            }
        except Exception as e:
            return {
                'response': f'Error al recuperar los detalles del informe: {str(e)}',
                'msg': self.FAILURE,
                'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
            }