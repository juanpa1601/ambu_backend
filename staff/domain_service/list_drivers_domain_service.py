from django.db.models import QuerySet
from staff.models import Driver
from staff.serializers.out import DriverSerializer
from staff.types.dataclass import DriverResponse

class ListDriversDomainService:
    '''
    Domain service for listing active drivers.
    
    Handles the core business logic for retrieving driver data.
    '''
    
    @staticmethod
    def get_active_drivers() -> list[DriverResponse]:
        '''
        Retrieve all active drivers from the database.
        
        Returns:
            list[DriverResponse]: List of active driver data dictionaries
        '''
        drivers: QuerySet[Driver] = Driver.objects.select_related(
            'base_staff',
            'base_staff__system_user'
        ).order_by('base_staff__system_user__first_name')
        serializer: DriverSerializer = DriverSerializer(
            drivers, 
            many=True
        )
        return serializer.data