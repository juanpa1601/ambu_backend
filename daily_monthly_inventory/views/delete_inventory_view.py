from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from typing import Any
from core.views.base_view import BaseView
from daily_monthly_inventory.application_service.delete_inventory_application_service import (
    DeleteInventoryApplicationService
)


class DeleteInventoryView(BaseView):
    '''
    API endpoint to delete an existing daily/monthly inventory.
    
    DELETE /daily_monthly_inventory/<inventory_id>/delete_inventory/
    
    Headers:
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
    
    Path Parameters:
        inventory_id (int): ID of the inventory to delete
    
    Success Response (200 OK):
        {
            "response": "Inventario eliminado exitosamente.",
            "msg": 1,
            "status_code": 200,
            "data": {
                "inventory_id": 1,
                "deleted": true
            }
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
            "response": "Ocurrió un error al eliminar el inventario.",
            "msg": -1,
            "status_code": 500
        }
    '''
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def delete(self, request: Request, inventory_id: int) -> Response:
        '''
        Handle DELETE request to remove an inventory.
        
        Args:
            request: HTTP request object
            inventory_id: ID of the inventory to delete
            
        Returns:
            Response confirming deletion
        '''
        return self._handle_request(
            request=request,
            serializer_class=None,
            service_method_callback=lambda user: self._delete_inventory_callback(
                user, inventory_id
            ),
            requires_auth=True
        )
    
    def _delete_inventory_callback(
        self, 
        user: User,
        inventory_id: int
    ) -> dict[str, Any]:
        '''
        Callback to execute delete inventory application service.
        
        Args:
            user: Authenticated user
            inventory_id: ID of the inventory to delete
            
        Returns:
            dictionary with response data
        '''
        application_service = DeleteInventoryApplicationService()
        return application_service.delete_inventory(
            inventory_id=inventory_id,
            requesting_user=user
        )
