from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from typing import Any
from core.views.base_view import BaseView
from daily_monthly_inventory.application_service.update_inventory_application_service import (
    UpdateInventoryApplicationService,
)
from daily_monthly_inventory.serializers.input.update_inventory_serializer import (
    UpdateInventorySerializer,
)


class UpdateInventoryView(BaseView):
    """
    API endpoint to partially update an existing daily/monthly inventory.

    PATCH /daily_monthly_inventory/<inventory_id>/update_inventory/

    Headers:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        Content-Type: application/json

    Path Parameters:
        inventory_id (int): ID of the inventory to update

    Request Body (all fields optional):
        {
            "date": "2026-01-21",
            "ambulance_id": 2,
            "observations": "Updated observations",
            "biomedical_equipment": {
                "field1": "value1",
                "field2": "value2"
            },
            "surgical": { ... },
            "respiratory": { ... },
            "immobilization_and_safety": { ... },
            "accessories": { ... },
            "additionals": { ... },
            "pediatric": { ... },
            "circulatory": { ... },
            "ambulance_kit": { ... },
            "accessories_case": { ... }
        }

    Success Response (200 OK):
        {
            "response": "Inventario actualizado exitosamente.",
            "msg": 1,
            "status_code": 200,
            "data": {
                "inventory_id": 1,
                "date": "2026-01-21",
                "observations": "Updated observations",
                "fields_updated": ["date", "ambulance", "observations", "biomedical_equipment"]
            }
        }

    Error Response (400 Bad Request - No fields provided):
        {
            "response": "Debe proporcionar al menos un campo para actualizar.",
            "msg": -1,
            "status_code": 400
        }

    Error Response (404 Not Found):
        {
            "response": "Inventario con ID 999 no encontrado.",
            "msg": -1,
            "status_code": 404
        }

    Error Response (401 Unauthorized):
        {
            "response": "Authentication credentials were not provided.",
            "msg": -1,
            "status_code": 401
        }

    Error Response (500 Internal Server Error):
        {
            "response": "Ocurrió un error al actualizar el inventario.",
            "msg": -1,
            "status_code": 500
        }
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, inventory_id: int) -> Response:
        """
        Handle PATCH request to partially update an inventory.

        Args:
            request: HTTP request object
            inventory_id: ID of the inventory to update

        Returns:
            Response with updated inventory data
        """
        return self._handle_request(
            request=request,
            serializer_class=UpdateInventorySerializer,
            service_method_callback=lambda validated_data,
            user: self._update_inventory_callback(validated_data, user, inventory_id),
            requires_auth=True,
        )

    def _update_inventory_callback(
        self, validated_data: dict[str, Any], user: User, inventory_id: int
    ) -> dict[str, Any]:
        """
        Callback to execute update inventory application service.

        Args:
            user: Authenticated user
            validated_data: Validated data from serializer
            inventory_id: ID of the inventory to update

        Returns:
            dictionary with response data
        """
        application_service = UpdateInventoryApplicationService()
        return application_service.update_inventory(
            inventory_id=inventory_id, update_data=validated_data, requesting_user=user
        )
