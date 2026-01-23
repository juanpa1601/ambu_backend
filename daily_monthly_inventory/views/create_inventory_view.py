from typing import Any

from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.views.base_view import BaseView
from daily_monthly_inventory.application_service import (
    CreateInventoryApplicationService,
)

# from daily_monthly_inventory.application_service.create_inventory_application_service import (
#     CreateInventoryApplicationService,
# )
from daily_monthly_inventory.serializers.input import CreateInventorySerializer

# from daily_monthly_inventory.serializers.input.create_inventory_serializer import (
#     CreateInventorySerializer,
# )


class CreateInventoryView(BaseView):
    """
    API endpoint to create a single daily/monthly inventory.
    POST /api/daily_monthly_inventory/create_inventory/
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(
        self,
        request: Request,
    ) -> Response:
        return self._handle_request(
            request=request,
            serializer_class=CreateInventorySerializer,
            service_method_callback=self._create_inventory_callback,
            requires_auth=True,
        )

    def _create_inventory_callback(
        self,
        validated_data: dict[str, Any],
        user: User,
    ) -> dict[str, Any]:
        create_inventory_service: CreateInventoryApplicationService = (
            CreateInventoryApplicationService()
        )
        return create_inventory_service.create_inventory(
            requesting_user=user, validated_data=validated_data
        )
