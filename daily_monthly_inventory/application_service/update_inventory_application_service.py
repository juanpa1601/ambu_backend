from typing import Any
import logging
from django.contrib.auth.models import User
from daily_monthly_inventory.models import (
    DailyMonthlyInventory,
    Ambulance,
    BiomedicalEquipment,
    Surgical,
    AccessoriesCase,
    Respiratory,
    ImmobilizationAndSafety,
    Accessories,
    Additionals,
    Pediatric,
    Circulatory,
    AmbulanceKit,
)


class UpdateInventoryApplicationService:
    """
    Application service for updating inventory information.
    Handles orchestration of inventory update operations.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def update_inventory(
        self, inventory_id: int, update_data: dict[str, Any], requesting_user: User
    ) -> dict[str, Any]:
        """
        Update inventory information.

        Args:
            inventory_id: ID of the inventory to update
            update_data: Dictionary with fields to update
            requesting_user: User making the request

        Returns:
            dictionary with response data and status
        """
        try:
            # Step 1: Get the inventory
            try:
                inventory = DailyMonthlyInventory.objects.select_related(
                    "biomedical_equipment",
                    "surgical",
                    "accessories_case",
                    "respiratory",
                    "immobilization_and_safety",
                    "accessories",
                    "additionals",
                    "pediatric",
                    "circulatory",
                    "ambulance_kit",
                    "ambulance",
                ).get(id=inventory_id)
            except DailyMonthlyInventory.DoesNotExist:
                self.logger.warning(
                    f"User {requesting_user.username} attempted to update non-existent inventory {inventory_id}"
                )
                return {
                    "response": f"Inventario con ID {inventory_id} no encontrado.",
                    "msg": -1,
                    "status_code_http": 404,
                }

            # Step 2: Track which fields are being updated
            updated_fields = []

            # Step 3: Update simple fields
            if "date" in update_data:
                inventory.date = update_data["date"]
                updated_fields.append("date")

            if "observations" in update_data:
                inventory.observations = update_data["observations"]
                updated_fields.append("observations")

            # Step 4: Update ambulance if provided
            if "ambulance_id" in update_data:
                if update_data["ambulance_id"] is None:
                    inventory.ambulance = None
                    updated_fields.append("ambulance")
                else:
                    try:
                        ambulance = Ambulance.objects.get(
                            pk=update_data["ambulance_id"]
                        )
                        inventory.ambulance = ambulance
                        updated_fields.append("ambulance")
                    except Ambulance.DoesNotExist:
                        return {
                            "response": f"Ambulancia con ID {update_data['ambulance_id']} no encontrada.",
                            "msg": -1,
                            "status_code_http": 400,
                        }

            # Step 5: Update related objects (create new or update existing)
            if "biomedical_equipment" in update_data:
                if inventory.biomedical_equipment:
                    for key, value in update_data["biomedical_equipment"].items():
                        setattr(inventory.biomedical_equipment, key, value)
                    inventory.biomedical_equipment.save()
                else:
                    inventory.biomedical_equipment = BiomedicalEquipment.objects.create(
                        **update_data["biomedical_equipment"]
                    )
                updated_fields.append("biomedical_equipment")

            if "surgical" in update_data:
                if inventory.surgical:
                    for key, value in update_data["surgical"].items():
                        setattr(inventory.surgical, key, value)
                    inventory.surgical.save()
                else:
                    inventory.surgical = Surgical.objects.create(
                        **update_data["surgical"]
                    )
                updated_fields.append("surgical")

            if "accessories_case" in update_data:
                if inventory.accessories_case:
                    for key, value in update_data["accessories_case"].items():
                        setattr(inventory.accessories_case, key, value)
                    inventory.accessories_case.save()
                else:
                    inventory.accessories_case = AccessoriesCase.objects.create(
                        **update_data["accessories_case"]
                    )
                updated_fields.append("accessories_case")

            if "respiratory" in update_data:
                if inventory.respiratory:
                    for key, value in update_data["respiratory"].items():
                        setattr(inventory.respiratory, key, value)
                    inventory.respiratory.save()
                else:
                    inventory.respiratory = Respiratory.objects.create(
                        **update_data["respiratory"]
                    )
                updated_fields.append("respiratory")

            if "immobilization_and_safety" in update_data:
                if inventory.immobilization_and_safety:
                    for key, value in update_data["immobilization_and_safety"].items():
                        setattr(inventory.immobilization_and_safety, key, value)
                    inventory.immobilization_and_safety.save()
                else:
                    inventory.immobilization_and_safety = (
                        ImmobilizationAndSafety.objects.create(
                            **update_data["immobilization_and_safety"]
                        )
                    )
                updated_fields.append("immobilization_and_safety")

            if "accessories" in update_data:
                if inventory.accessories:
                    for key, value in update_data["accessories"].items():
                        setattr(inventory.accessories, key, value)
                    inventory.accessories.save()
                else:
                    inventory.accessories = Accessories.objects.create(
                        **update_data["accessories"]
                    )
                updated_fields.append("accessories")

            if "additionals" in update_data:
                if inventory.additionals:
                    for key, value in update_data["additionals"].items():
                        setattr(inventory.additionals, key, value)
                    inventory.additionals.save()
                else:
                    inventory.additionals = Additionals.objects.create(
                        **update_data["additionals"]
                    )
                updated_fields.append("additionals")

            if "pediatric" in update_data:
                if inventory.pediatric:
                    for key, value in update_data["pediatric"].items():
                        setattr(inventory.pediatric, key, value)
                    inventory.pediatric.save()
                else:
                    inventory.pediatric = Pediatric.objects.create(
                        **update_data["pediatric"]
                    )
                updated_fields.append("pediatric")

            if "circulatory" in update_data:
                if inventory.circulatory:
                    for key, value in update_data["circulatory"].items():
                        setattr(inventory.circulatory, key, value)
                    inventory.circulatory.save()
                else:
                    inventory.circulatory = Circulatory.objects.create(
                        **update_data["circulatory"]
                    )
                updated_fields.append("circulatory")

            if "ambulance_kit" in update_data:
                if inventory.ambulance_kit:
                    for key, value in update_data["ambulance_kit"].items():
                        setattr(inventory.ambulance_kit, key, value)
                    inventory.ambulance_kit.save()
                else:
                    inventory.ambulance_kit = AmbulanceKit.objects.create(
                        **update_data["ambulance_kit"]
                    )
                updated_fields.append("ambulance_kit")

            # Step 6: Save inventory
            inventory.save()

            # Step 7: Build response
            self.logger.info(
                f"User {requesting_user.username} successfully updated inventory {inventory_id}. "
                f"Fields updated: {', '.join(updated_fields)}"
            )

            return {
                "response": "Inventario actualizado exitosamente.",
                "msg": 1,
                "status_code_http": 200,
                "data": {
                    "inventory_id": inventory.id,
                    "date": inventory.date.isoformat(),
                    "observations": inventory.observations,
                    "fields_updated": updated_fields,
                },
            }

        except Exception as e:
            self.logger.error(
                f"Error updating inventory {inventory_id} for {requesting_user.username}: {str(e)}",
                exc_info=True,
            )
            return {
                "response": "Ocurrió un error al actualizar el inventario.",
                "msg": -1,
                "status_code_http": 500,
            }
