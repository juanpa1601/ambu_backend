from typing import Any
from django.contrib.auth.models import User
from django.db.models import QuerySet
from ..models import PatientTransportReport
from ..serializers.out import PatientTransportReportSummarySerializer
from staff.models import Administrative
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)

class ListReportsApplicationService:
    '''
    Application service for listing ALL transport reports.
    
    Business logic:
    - Administrative staff can view all reports (not filtered by created_by)
    - Separate reports by status (draft vs completed)
    - Order by most recent first
    - Include related patient and creator info
    '''
    
    SUCCESS: int = 1
    FAILURE: int = -1     

    def list_all_reports(
        self, 
        user: User
    ) -> dict[str, Any]:
        '''    
        List ALL transport reports (for administrative staff).
        
        Filters:
        - None (retrieves all reports)
        - Separated by status: 'borrador' and 'completado'
        
        Args:
            user: Authenticated user making the request
        
        Returns:
            dict: {
                'response': Success/error message
                'msg': 1 for success, -1 for error
                'status_code_http': HTTP status code
                'list_reports': List of all reports
                'total_reports': Total count of reports
            }
        
        Raises:
            Exception: If database query fails
        '''
        try:
            # Verify user has permission (Administrative only)
            is_administrative: bool = Administrative.objects.filter(
                base_staff__system_user=user
            ).exists()
            if not is_administrative:
                return {
                    'response': 'Solamente el personal administrativo puede acceder a este recurso.',
                    'msg': self.FAILURE,
                    'status_code_http': HTTP_403_FORBIDDEN
                }
            all_reports: QuerySet[PatientTransportReport] = PatientTransportReport.objects.all().select_related(
                'patient',
                'created_by',
                'updated_by'
            ).order_by('-created_at')
            all_reports_serializer: PatientTransportReportSummarySerializer = PatientTransportReportSummarySerializer(
                all_reports,
                many=True
            )
            return {
                'response': 'Éxito al recuperar todos los informes.',
                'msg': self.SUCCESS,
                'status_code_http': HTTP_200_OK,
                'list_reports': all_reports_serializer.data,
                'total_reports': all_reports.count()
            }
        except Exception as e:
            return {
                'response': f'Error al recuperar los informes: {str(e)}',
                'msg': self.FAILURE,
                'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
            }