from typing import Any

from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.views.base_view import BaseView
from daily_monthly_inventory.application_service import SaveInventoryApplicationService
from daily_monthly_inventory.serializers.input import UpdateInventorySerializer


class SaveInventoryView(BaseView):
    """
    API endpoint to create or update daily/monthly inventory.
    Unified endpoint supporting both creation and updates with partial saves (draft mode).
    
    POST /daily_monthly_inventory/save_inventory/
    
    Headers:
        Authorization: Token <token_value>
        Content-Type: application/json
    
    Request Body (CREATE - inventory_id = null):
        {
            "inventory_id": null,
            "date": "2026-01-30",
            "ambulance_id": 2,
            "shift": {"id": 1},
            "support_staff": "Juan Pérez",
            "observations": "",
            "biomedical_equipment": {
                "monitor": 2,
                "aed": 1,
                ...
            },
            "surgical": {...},
            ...
        }
    
    Request Body (UPDATE - inventory_id = <int>):
        {
            "inventory_id": 123,
            "biomedical_equipment": {
                "monitor": 3
            },
            "observations": "Actualizado"
        }
    
    Request Body (PARTIAL SAVE - Draft mode):
        {
            "inventory_id": null,  // or <int> for update
            "date": "2026-01-30",
            "ambulance_id": 2,
            // Only some sections filled - others can be null/empty
            "biomedical_equipment": {...}
        }
    
    Success Response (201 Created - new):
        {
            "response": "Inventario creado exitosamente.",
            "msg": 1,
            "status_code_http": 201,
            "data": {
                "inventory_id": 123
            }
        }
    
    Success Response (200 OK - update):
        {
            "response": "Inventario actualizado exitosamente.",
            "msg": 1,
            "status_code_http": 200,
            "data": {
                "inventory_id": 123,
                "fields_updated": ["biomedical_equipment", "observations"]
            }
        }
    
    Error Response (400 Bad Request):
        {
            "response": "Ya existe un inventario para la ambulancia...",
            "msg": -1,
            "status_code_http": 400
        }
    
    Error Response (404 Not Found):
        {
            "response": "Inventario con ID 123 no encontrado.",
            "msg": -1,
            "status_code_http": 404
        }
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Save inventory (create new or update existing).
        
        Supports:
        - CREATE: inventory_id = null + required fields
        - UPDATE: inventory_id = <int> + any fields to update
        - PARTIAL SAVE: Works with incomplete data (draft mode)
        """
        return self._handle_request(
            request=request,
            serializer_class=UpdateInventorySerializer,
            service_method_callback=self._save_inventory_callback,
            requires_auth=True,
        )

    def _save_inventory_callback(
        self,
        validated_data: dict[str, Any],
        user: User,
    ) -> dict[str, Any]:
        """
        Execute business logic to save inventory.
        
        Args:
            validated_data: Validated and serialized request data
            user: Authenticated user making the request
            
        Returns:
            dict: Service response with inventory data
        """
        save_inventory_service: SaveInventoryApplicationService = (
            SaveInventoryApplicationService()
        )
        return save_inventory_service.save_inventory(
            data=validated_data,
            user=user,
        )
