from typing import Any
from django.contrib.auth.models import User
from staff.domain_service import ListDriversDomainService
from staff.types.dataclass import DriverResponse

class ListDriversApplicationService:
    '''|
    Application service for listing drivers.
    
    Orchestrates the process of retrieving active drivers.
    No special permissions required - all authenticated users can view drivers.
    '''
    
    def list_drivers(
        self, 
        user: User
    ) -> dict[str, Any]:
        '''
        List all active drivers in the system.
        
        Args:
            user: Authenticated user making the request
        
        Returns:
            dict: {
                'response': 'Mensaje de éxito',
                'msg': 1 for success
                'status_code': HTTP status code
                'drivers': List of driver data
                'total_count': Total number of active drivers
            }
        '''
        try:
            # Get active drivers from domain service
            drivers: list[DriverResponse] = ListDriversDomainService.get_active_drivers()
            return {
                'response': 'Conductores recuperados exitosamente.',
                'msg': 1,
                'status_code': 200,
                'drivers': drivers,
                'total_count': len(drivers)
            }
        except Exception as e:
            return {
                'response': f'Error al recuperar conductores: {str(e)}',
                'msg': -1,
                'status_code': 500
            }