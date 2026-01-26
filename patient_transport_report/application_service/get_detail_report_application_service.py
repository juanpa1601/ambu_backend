from typing import Any
from django.contrib.auth.models import User
from ..models import PatientTransportReport
from ..serializers.out import PatientTransportReportDetailSerializer
from staff.models import (
    Healthcare, 
    Administrative
)

class GetDetailsReportApplicationService:
    '''
    Application service for retrieving detailed patient transport report.
    
    Business logic:
    - Verify user is Healthcare or Administrative staff
    - Retrieve complete report with all nested relationships
    - Return full serialized data
    '''
    
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
            is_healthcare: bool = Healthcare.objects.filter(user=user).exists()
            is_administrative: bool = Administrative.objects.filter(user=user).exists()
            if not (is_healthcare or is_administrative):
                return {
                    'response': 'Solamente el personal de salud o administrativo puede acceder a este recurso.',
                    'msg': -1,
                    'status_code_http': 403
                }                
            # Retrieve report with all relationships using select_related and prefetch_related
            report: PatientTransportReport = PatientTransportReport.objects.select_related(
                'patient',
                'patient__insurance_provider',
                'informed_consent',
                'informed_consent__companion',
                'informed_consent__healthcare_staff',
                'informed_consent__outgoing_entity',
                'informed_consent__receiving_entity',
                'care_transfer_report',
                'care_transfer_report__driver',
                'care_transfer_report__attending_staff',
                'care_transfer_report__support_staff',
                'care_transfer_report__ambulance',
                'care_transfer_report__companion_1',
                'care_transfer_report__companion_2',
                'care_transfer_report__initial_physicial_examination',
                'care_transfer_report__final_physical_examination',
                'care_transfer_report__treatment',
                'care_transfer_report__diagnosis_1',
                'care_transfer_report__diagnosis_2',
                'care_transfer_report__result',
                'care_transfer_report__complications_transfer',
                'care_transfer_report__receiving_entity',
                'satisfaction_survey',
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
                'msg': 1,
                'status_code_http': 200,
                'report': serializer.data
            }
        except PatientTransportReport.DoesNotExist:
            return {
                'response': f'Informe con ID {report_id} no encontrado.',
                'msg': -1,
                'status_code_http': 404
            }
        except Exception as e:
            return {
                'response': f'Error al recuperar los detalles del informe: {str(e)}',
                'msg': -1,
                'status_code_http': 500
            }