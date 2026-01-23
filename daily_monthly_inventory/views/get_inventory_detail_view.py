from typing import Any

from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.views.base_view import BaseView
from daily_monthly_inventory.application_service import (
    GetInventoryDetailApplicationService,
)


class GetInventoryDetailView(BaseView):
    """
    API endpoint to get detailed information for a specific daily/monthly inventory.

    GET /api/daily_monthly_inventory/<int:inventory_id>/get_detail/

    Headers:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

    Success Response (200 OK):
        {
            "response": "Inventario recuperado exitosamente.",
            "msg": 1,
            "status_code": 200,
            "data": {
                "inventory_id": 1,
                "system_user_id": 1,
                "person_name": "Dr. Juan Pérez",
                "date": "2026-01-20",
                "observations": "Inventario completo",
                "ambulance_id": 1,
                "ambulance_mobile_number": "12345",
                "biomedical_equipment_id": 1,
                "surgical_id": 1,
                "accessories_case_id": 1,
                "respiratory_id": 1,
                "immobilization_and_safety_id": 1,
                "accessories_id": 1,
                "additionals_id": 1,
                "pediatric_id": 1,
                "circulatory_id": 1,
                "ambulance_kit_id": 1,
                "created_at": "2026-01-20T10:30:00"
            }
        }

    Error Response (404 Not Found):
        {
            "response": "Inventario no encontrado.",
            "msg": -1,
            "status_code": 404
        }
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(
        self,
        request: Request,
        inventory_id: int,
    ) -> Response:
        """
        Handle GET request to retrieve inventory details.

        Args:
            request: HTTP request object
            inventory_id: ID of the inventory to retrieve

        Returns:
            Response with inventory detail data
        """
        return self._handle_request(
            request=request,
            serializer_class=None,
            service_method_callback=lambda user: self._get_detail_callback(
                user,
                inventory_id,
            ),
            requires_auth=True,
        )

    def _get_detail_callback(
        self,
        user: User,
        inventory_id: int,
    ) -> dict[str, Any]:
        """
        Callback to execute inventory detail retrieval logic.

        Args:
            user: Authenticated user making the request
            inventory_id: ID of the inventory to retrieve

        Returns:
            Dictionary with response data
        """
        get_inventory_detail_service: GetInventoryDetailApplicationService = (
            GetInventoryDetailApplicationService()
        )
        return get_inventory_detail_service.get_inventory_detail(
            requesting_user=user, inventory_id=inventory_id
        )
