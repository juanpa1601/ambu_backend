from typing import Any

from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.views.base_view import BaseView
from daily_monthly_inventory.application_service import ListInventoryApplicationService


class ListInventoryView(BaseView):
    """
    API endpoint to list all daily/monthly inventories.

    GET /api/daily_monthly_inventory/list_inventories/

    Headers:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

    Success Response (200 OK):
        {
            "response": "Inventarios recuperados exitosamente.",
            "msg": 1,
            "status_code": 200,
            "data": {
                "inventories": [
                    {
                        "inventory_id": 1,
                        "person_name": "Dr. Juan Pérez",
                        "mobile_number": "+51987654321",
                        "date": "2026-01-15"
                    },
                    {
                        "inventory_id": 2,
                        "person_name": "Carlos Rodríguez",
                        "mobile_number": "+51912345678",
                        "date": "2026-01-20"
                    }
                ],
                "total_count": 2
            }
        }

    Error Response (401 Unauthorized):
        {
            "response": "Authentication credentials were not provided.",
            "msg": -1,
            "status_code": 401
        }

    Error Response (500 Internal Server Error):
        {
            "response": "Ocurrió un error al recuperar los inventarios.",
            "msg": -1,
            "status_code": 500
        }
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        Handle GET request to list all inventories.

        Args:
            request: HTTP request object

        Returns:
            Response with inventory data
        """
        return self._handle_request(
            request=request,
            serializer_class=None,
            service_method_callback=self._list_inventories_callback,
            requires_auth=True,
        )

    def _list_inventories_callback(self, user: User) -> dict[str, Any]:
        """
        Callback to execute inventory listing logic.

        Args:
            user: Authenticated user making the request

        Returns:
            Dictionary with response data
        """
        list_inventory_service: ListInventoryApplicationService = (
            ListInventoryApplicationService()
        )
        return list_inventory_service.list_inventories(requesting_user=user)
