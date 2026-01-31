import logging
from typing import Any

from django.contrib.auth.models import User
from django.db import transaction

from daily_monthly_inventory.domain_service import InventoryDomainService
from daily_monthly_inventory.models import (
    Ambulance,
    DailyMonthlyInventory,
    Shift,
)
from daily_monthly_inventory.types.dataclass import (
    CreateInventoryRequest,
    UpdateInventoryRequest,
)


class SaveInventoryApplicationService:
    """
    Application service for saving (creating or updating) inventory information.
    Supports partial saves (draft mode) and final submission.
    Unified endpoint similar to SaveReportApplicationService.
    """

    SUCCESS: int = 1
    FAILURE: int = -1

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        self.inventory_domain_service: InventoryDomainService = InventoryDomainService()

    @transaction.atomic
    def save_inventory(
        self,
        data: dict[str, Any],
        user: User,
    ) -> dict[str, Any]:
        """
        Save inventory (create new or update existing).
        
        Args:
            data: Request data with inventory_id and inventory fields
            user: User making the request
            
        Returns:
            dict: Response with status and inventory data
        """
        inventory_id: int | None = data.get("inventory_id")
        
        self.logger.info(
            f"save_inventory called by {user.username} - inventory_id: {inventory_id} "
            f"(type: {type(inventory_id)})"
        )
        
        try:
            if inventory_id is None:
                # CREATE new inventory
                self.logger.info("Creating new inventory")
                return self._create_new_inventory(data, user)
            else:
                # UPDATE existing inventory
                self.logger.info(f"Updating existing inventory {inventory_id}")
                return self._update_existing_inventory(inventory_id, data, user)
                
        except DailyMonthlyInventory.DoesNotExist:
            self.logger.warning(
                f"User {user.username} attempted to update non-existent inventory {inventory_id}"
            )
            return {
                "response": f"Inventario con ID {inventory_id} no encontrado.",
                "msg": self.FAILURE,
                "status_code_http": 404,
            }
            
        except Ambulance.DoesNotExist:
            self.logger.warning(f"Ambulance not found while saving inventory")
            return {
                "response": "Ambulancia especificada no encontrada.",
                "msg": self.FAILURE,
                "status_code_http": 404,
            }
            
        except Shift.DoesNotExist:
            self.logger.warning(f"Shift not found while saving inventory")
            return {
                "response": "Jornada especificada no encontrada.",
                "msg": self.FAILURE,
                "status_code_http": 404,
            }
            
        except Exception as e:
            self.logger.error(f"Error saving inventory: {str(e)}", exc_info=True)
            return {
                "response": f"Error al guardar el inventario: {str(e)}",
                "msg": self.FAILURE,
                "status_code_http": 500,
            }

    def _create_new_inventory(
        self,
        data: dict[str, Any],
        user: User,
    ) -> dict[str, Any]:
        """
        Create new inventory with provided data.
        Supports partial data (draft mode).
        """
        try:
            # Build CreateInventoryRequest DTO
            request_dto: CreateInventoryRequest = CreateInventoryRequest(
                system_user_id=user.id,
                ambulance_id=data.get("ambulance_id"),
                shift_id=data.get("shift", {}).get("id") if data.get("shift") else None,
                date=data.get("date"),
                observations=data.get("observations", ""),
                support_staff=data.get("support_staff"),
                biomedical_equipment=data.get("biomedical_equipment"),
                surgical=data.get("surgical"),
                accessories_case=data.get("accessories_case"),
                respiratory=data.get("respiratory"),
                immobilization_and_safety=data.get("immobilization_and_safety"),
                accessories=data.get("accessories"),
                additionals=data.get("additionals"),
                pediatric=data.get("pediatric"),
                circulatory=data.get("circulatory"),
                ambulance_kit=data.get("ambulance_kit"),
            )

            # Create inventory using domain service
            response_dto = self.inventory_domain_service.create_inventory(request_dto)

            self.logger.info(
                f"User {user.username} created new inventory {response_dto.inventory_id}"
            )

            return {
                "response": "Inventario creado exitosamente.",
                "msg": self.SUCCESS,
                "status_code_http": 201,
                "data": {
                    "inventory_id": response_dto.inventory_id,
                },
            }

        except ValueError as e:
            # Validation errors (e.g., duplicate inventory)
            self.logger.warning(f"Validation error creating inventory: {str(e)}")
            return {
                "response": str(e),
                "msg": self.FAILURE,
                "status_code_http": 400,
            }

    def _update_existing_inventory(
        self,
        inventory_id: int,
        data: dict[str, Any],
        user: User,
    ) -> dict[str, Any]:
        """
        Update existing inventory with provided data.
        Supports partial updates (only provided fields are updated).
        """
        try:
            # Verify inventory exists
            inventory = DailyMonthlyInventory.objects.get(pk=inventory_id)

            # Build UpdateInventoryRequest DTO
            request_dto: UpdateInventoryRequest = UpdateInventoryRequest(
                inventory_id=inventory_id,
                date=data.get("date"),
                observations=data.get("observations"),
                ambulance_id=data.get("ambulance_id"),
                shift_id=data.get("shift", {}).get("id") if data.get("shift") else None,
                support_staff=data.get("support_staff"),
                biomedical_equipment=data.get("biomedical_equipment"),
                surgical=data.get("surgical"),
                accessories_case=data.get("accessories_case"),
                respiratory=data.get("respiratory"),
                immobilization_and_safety=data.get("immobilization_and_safety"),
                accessories=data.get("accessories"),
                additionals=data.get("additionals"),
                pediatric=data.get("pediatric"),
                circulatory=data.get("circulatory"),
                ambulance_kit=data.get("ambulance_kit"),
            )

            # Update inventory using domain service
            response_dto = self.inventory_domain_service.update_inventory(request_dto)

            self.logger.info(
                f"User {user.username} updated inventory {inventory_id}. Fields: {response_dto.fields_updated}"
            )

            return {
                "response": "Inventario actualizado exitosamente.",
                "msg": self.SUCCESS,
                "status_code_http": 200,
                "data": {
                    "inventory_id": response_dto.inventory_id,
                    "fields_updated": response_dto.fields_updated,
                },
            }

        except ValueError as e:
            self.logger.warning(f"Validation error updating inventory: {str(e)}")
            return {
                "response": str(e),
                "msg": self.FAILURE,
                "status_code_http": 400,
            }
