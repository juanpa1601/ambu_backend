from typing import Any
import logging
from django.contrib.auth.models import User
from daily_monthly_inventory.domain_service import InventoryDomainService
from daily_monthly_inventory.types.dataclass import (
    CreateInventoryRequest,
    CreateInventoryResponse
)


class CreateInventoryApplicationService:
    '''Application service for creating a single inventory.'''

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.inventory_domain_service: InventoryDomainService = InventoryDomainService()

    def create_inventory(self, requesting_user: User, validated_data: dict[str, Any]) -> dict[str, Any]:
        try:
            # Build request DTO using the authenticated user as system_user
            request_dto = CreateInventoryRequest(
                system_user_id=requesting_user.id,
                date=validated_data['date'],
                ambulance_id=validated_data.get('ambulance_id'),
                biomedical_equipment=validated_data.get('biomedical_equipment'),
                surgical=validated_data.get('surgical'),
                accessories_case=validated_data.get('accessories_case'),
                respiratory=validated_data.get('respiratory'),
                immobilization_and_safety=validated_data.get('immobilization_and_safety'),
                accessories=validated_data.get('accessories'),
                additionals=validated_data.get('additionals'),
                pediatric=validated_data.get('pediatric'),
                circulatory=validated_data.get('circulatory'),
                ambulance_kit=validated_data.get('ambulance_kit'),
                observations=validated_data.get('observations', '')
            )

            response_dto: CreateInventoryResponse = self.inventory_domain_service.create_inventory(request_dto)

            return {
                'response': 'Inventario creado exitosamente.',
                'msg': 1,
                'status_code_http': 201,
                'data': {
                    'inventory_id': response_dto.inventory_id
                }
            }
        except Exception as e:
            self.logger.error(f'Error creating inventory for user {requesting_user.username}: {str(e)}', exc_info=True)
            return {
                'response': 'Ocurrió un error al crear el inventario.',
                'msg': -1,
                'status_code_http': 500
            }
