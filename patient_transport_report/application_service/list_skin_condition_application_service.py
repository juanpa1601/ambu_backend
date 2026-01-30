from typing import Any
from django.db.models import QuerySet
from patient_transport_report.models import SkinCondition
from patient_transport_report.serializers.out import SkinConditionDetailSerializer
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_500_INTERNAL_SERVER_ERROR
)

class ListSkinConditionApplicationService:
    '''
    Application service for listing all skin conditions.
    
    Business logic:
    - Retrieve all active skin conditions ordered by 'order' field
    - Serialize data for API response
    - Return structured response
    '''
    
    SUCCESS: int = 1
    FAILURE: int = -1

    def list_skin_conditions(self) -> dict[str, Any]:
        '''
        List all skin conditions ordered by display order.
        
        Returns:
            dict: {
                'response': Success/error message
                'msg': 1 for success, -1 for error
                'status_code_http': HTTP status code
                'data': {
                    'skin_conditions': List of skin condition objects
                    'total': Total count
                }
            }
        '''
        try:
            # Retrieve all skin conditions ordered by 'order' field
            skin_conditions: QuerySet[SkinCondition] = SkinCondition.objects.all().order_by('order')
            # Serialize data
            serializer: SkinConditionDetailSerializer = SkinConditionDetailSerializer(skin_conditions, many=True)
            return {
                'response': 'Condiciones de piel recuperadas exitosamente.',
                'msg': self.SUCCESS,
                'status_code_http': HTTP_200_OK,
                'data': {
                    'skin_conditions': serializer.data,
                    'total': skin_conditions.count()
                }
            }
        except Exception as e:
            return {
                'response': f'Error al recuperar condiciones de piel: {str(e)}',
                'msg': self.FAILURE,
                'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
            }