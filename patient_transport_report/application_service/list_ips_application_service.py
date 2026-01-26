from typing import Any
from django.db.models import QuerySet
from ..models import IPS
from ..serializers.out import IPSSerializer

class ListIPSApplicationService:
    '''
    Application service for listing active IPS (Receiving Institutions).
    
    Business logic:
    - Retrieve only active institutions (is_active=True)
    - Order alphabetically by name
    - Serialize data for API response
    '''
    
    def list_active_ips(self) -> dict[str, Any]:
        '''    
        List all active receiving institutions.
        
        Returns:
            dict: {
                'response': Success/error message
                'msg': 1 for success, -1 for error
                'status_code_http': HTTP status code
                'institutions': List of serialized IPS objects
                'total': Total count of active institutions
            }
        
        Raises:
            Exception: If database query fails
        '''
        try:
            # Get only active institutions ordered by name
            ips_list: QuerySet[IPS] = IPS.objects.filter(is_active=True).order_by('id')
            # Serialize data
            serializer: IPSSerializer = IPSSerializer(ips_list, many=True)
            return {
                'response': 'Successfully retrieved active institutions.',
                'msg': 1,
                'status_code_http': 200,
                'institutions': serializer.data,
                'total': ips_list.count()
            }
        except Exception as e:
            return {
                'response': f'Error retrieving institutions: {str(e)}',
                'msg': -1,
                'status_code_http': 500
            }