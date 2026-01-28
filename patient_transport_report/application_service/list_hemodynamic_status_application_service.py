from typing import Any
from patient_transport_report.models import HemodynamicStatus
from patient_transport_report.serializers.out import HemodynamicStatusDetailSerializer
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_500_INTERNAL_SERVER_ERROR
)
from django.db.models import QuerySet

class ListHemodynamicStatusApplicationService:
    '''
    Application service for listing all hemodynamic statuses.
    
    Business logic:
    - Retrieve all hemodynamic statuses ordered by 'order' field
    - Serialize data for API response
    - Return structured response
    '''
    
    SUCCESS: int = 1
    FAILURE: int = -1

    def list_hemodynamic_statuses(self) -> dict[str, Any]:
        '''
        List all hemodynamic statuses ordered by display order.
        
        Returns:
            dict: {
                'response': Success/error message
                'msg': 1 for success, -1 for error
                'status_code_http': HTTP status code
                'data': {
                    'hemodynamic_statuses': List of hemodynamic status objects
                    'total': Total count
                }
            }
        '''
        try:
            # Retrieve all hemodynamic statuses ordered by 'order' field
            hemodynamic_statuses: QuerySet[HemodynamicStatus] = HemodynamicStatus.objects.all().order_by('order')
            # Serialize data
            serializer: HemodynamicStatusDetailSerializer = HemodynamicStatusDetailSerializer(hemodynamic_statuses, many=True)
            return {
                'response': 'Estados hemodinámicos recuperados exitosamente.',
                'msg': self.SUCCESS,
                'status_code_http': HTTP_200_OK,
                'data': {
                    'hemodynamic_statuses': serializer.data,
                    'total': hemodynamic_statuses.count()
                }
            }
        except Exception as e:
            return {
                'response': f'Error al recuperar estados hemodinámicos: {str(e)}',
                'msg': self.FAILURE,
                'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
            }