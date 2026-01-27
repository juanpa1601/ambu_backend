from typing import Any

from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.views.base_view import BaseView
from daily_monthly_inventory.application_service import ListAmbulancesApplicationService


class ListAmbulancesView(BaseView):
    """
    API endpoint to list all active ambulances for dropdown menus.

    GET /api/daily_monthly_inventory/list_ambulances/

    Headers:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

    Success Response (200 OK):
        {
            "response": "Ambulancias recuperadas exitosamente.",
            "msg": 1,
            "status_code": 200,
            "data": {
                "ambulances": [
                    {
                        "id": 1,
                        "mobile_number": 1,
                        "license_plate": "ABC-123",
                        "display_name": "Móvil 1 - ABC-123"
                    },
                    {
                        "id": 2,
                        "mobile_number": 2,
                        "license_plate": "DEF-456",
                        "display_name": "Móvil 2 - DEF-456"
                    }
                ],
                "total_count": 2
            }
        }

    Error Response (401 Unauthorized):
        {
            "response": "No se proporcionaron credenciales de autenticación.",
            "msg": -1,
            "status_code": 401
        }

    Error Response (500 Internal Server Error):
        {
            "response": "Ocurrió un error al recuperar las ambulancias.",
            "msg": -1,
            "status_code": 500
        }
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(
        self,
        request: Request,
    ) -> Response:
        """
        Handle GET request to list all active ambulances.

        Args:
            request: HTTP request object

        Returns:
            Response with ambulances data
        """
        return self._handle_request(
            request=request,
            serializer_class=None,
            service_method_callback=self._list_ambulances_callback,
            requires_auth=True,
        )

    def _list_ambulances_callback(
        self,
        user: User,
    ) -> dict[str, Any]:
        """
        Callback to execute list ambulances application service.

        Args:
            user: Authenticated user

        Returns:
            dictionary with response data
        """
        list_ambulances_service: ListAmbulancesApplicationService = (
            ListAmbulancesApplicationService()
        )
        return list_ambulances_service.list_ambulances(requesting_user=user)
