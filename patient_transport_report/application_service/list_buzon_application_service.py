from typing import Any
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.db.models import QuerySet
from ..models import PatientTransportReport
from ..serializers.out import PatientTransportReportSummarySerializer
from staff.models import Healthcare

class ListBuzonApplicationService:
    '''
    Application service for listing user's own transport reports (inbox/buzon).
    
    Business logic:
    - Filter reports by logged-in user (created_by)
    - Filter reports created within last 48 hours
    - Separate reports by status (draft vs completed)
    - Order by most recent first
    '''
    
    def list_user_reports(
        self, 
        user: User
    ) -> dict[str, Any]:
        '''    
        List transport reports for the authenticated user.
        
        Filters:
        - created_by: Only reports created by the logged-in user
        - created_at: Only reports from the last 48 hours
        - Separated by status: 'borrador' and 'completado'
        
        Args:
            user: Authenticated user making the request
        
        Returns:
            dict: {
                'response': Success/error message
                'msg': 1 for success, -1 for error
                'status_code_http': HTTP status code
                'list_report_draft': List of draft reports
                'list_report_completed': List of completed reports
                'total_draft': Count of draft reports
                'total_completed': Count of completed reports
                'filter_hours': Number of hours filtered (48)
            }
        
        Raises:
            Exception: If database query fails
        '''
        try:
            # Verify user has permission (Healthcare or Administrative)
            is_healthcare: bool = Healthcare.objects.filter(user=user).exists()
            if not (is_healthcare):
                return {
                    'response': 'Solamente el personal de salud puede acceder a este recurso.',
                    'msg': -1,
                    'status_code_http': 403
                }                  
            # Calculate time threshold (48 hours ago)
            time_threshold: timezone.datetime = timezone.now() - timedelta(hours=48)
            # Base queryset: user's reports from last 48 hours
            base_queryset: QuerySet[PatientTransportReport] = PatientTransportReport.objects.filter(
                created_by=user,
                created_at__gte=time_threshold
            ).select_related(
                'patient',
                'created_by'
            ).order_by('-created_at')
            # Separate by status
            draft_reports: QuerySet[PatientTransportReport] = base_queryset.filter(status='borrador')
            completed_reports: QuerySet[PatientTransportReport] = base_queryset.filter(status='completado')
            # Serialize data
            draft_serializer: PatientTransportReportSummarySerializer = PatientTransportReportSummarySerializer(draft_reports, many=True)
            completed_serializer: PatientTransportReportSummarySerializer = PatientTransportReportSummarySerializer(completed_reports, many=True)
            return {
                'response': 'Exito al recuperar los informes del usuario.',
                'msg': 1,
                'status_code_http': 200,
                'list_report_draft': draft_serializer.data,
                'list_report_completed': completed_serializer.data,
                'total_draft': draft_reports.count(),
                'total_completed': completed_reports.count()
            }
        except Exception as e:
            return {
                'response': f'Error retrieving user reports: {str(e)}',
                'msg': -1,
                'status_code_http': 500
            }