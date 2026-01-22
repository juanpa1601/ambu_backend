import logging
from typing import Any

from django.contrib.auth.models import User

from daily_monthly_inventory.models import (
    Accessories,
    AccessoriesCase,
    Additionals,
    Ambulance,
    AmbulanceKit,
    BiomedicalEquipment,
    Circulatory,
    DailyMonthlyInventory,
    ImmobilizationAndSafety,
    Pediatric,
    Respiratory,
    Surgical,
)

from daily_monthly_inventory.types.dataclass import (
    CreateInventoryRequest,
    CreateInventoryResponse,
    InventoryDetailResponse,
    InventoryListItem,
    InventoryListResponse,
)


class EntityNotFoundError(Exception):
    """Base exception raised when a required domain entity is not found."""


class UserNotFoundError(EntityNotFoundError):
    """Raised when the requested user does not exist."""


class AmbulanceNotFoundError(EntityNotFoundError):
    """Raised when the requested ambulance does not exist or is missing."""


class InventoryDomainService:
    """Domain service for inventory-related operations."""

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

    def get_all_inventories(self) -> InventoryListResponse:
        """
        Retrieve all daily/monthly inventories with basic information.

        Returns:
            InventoryListResponse with list of inventory items
        """
        try:
            # Query all DailyMonthlyInventory with related system_user and ambulance
            inventories: list[DailyMonthlyInventory] = (
                DailyMonthlyInventory.objects.select_related(
                    "system_user", "ambulance"
                ).all()
            )

            inventory_items: list[InventoryListItem] = []

            for inventory in inventories:
                # Get person name from system_user
                person_name: str = ""
                if inventory.system_user:
                    user: User = inventory.system_user
                    person_name = user.get_full_name() or user.username

                # Get mobile_number from ambulance
                mobile_number: str = ""
                if inventory.ambulance:
                    mobile_number = str(inventory.ambulance.mobile_number)

                inventory_item: InventoryListItem = InventoryListItem(
                    inventory_id=inventory.pk,
                    person_name=person_name,
                    mobile_number=mobile_number,
                    date=inventory.date,
                )
                inventory_items.append(inventory_item)

            self.logger.info(f"Retrieved {len(inventory_items)} inventories")
            return InventoryListResponse(
                inventories=inventory_items, total_count=len(inventory_items)
            )

        except Exception as e:
            self.logger.error(f"Error retrieving inventories: {str(e)}", exc_info=True)
            raise

    def create_inventory(
        self,
        request: CreateInventoryRequest,
    ) -> CreateInventoryResponse:
        """
        Create a DailyMonthlyInventory using the provided request DTO.
        Creates new records for all related foreign key models.
        """
        try:
            # Resolve system user
            try:
                user: User = User.objects.get(id=request.system_user_id)
            except User.DoesNotExist:
                self.logger.error(
                    f"User with ID {request.system_user_id} does not exist",
                    exc_info=True,
                )
                raise UserNotFoundError(
                    f"User with ID {request.system_user_id} does not exist"
                )

            # Resolve ambulance by ID (required)
            if not request.ambulance_id:
                self.logger.error("Ambulance id is required to create inventory")
                raise AmbulanceNotFoundError(
                    "Ambulance id is required to create inventory"
                )

            try:
                ambulance: Ambulance = Ambulance.objects.get(id=request.ambulance_id)
            except Ambulance.DoesNotExist:
                self.logger.error(
                    f"Ambulance with ID {request.ambulance_id} does not exist",
                    exc_info=True,
                )
                raise AmbulanceNotFoundError(
                    f"Ambulance with ID {request.ambulance_id} does not exist"
                )

            # Create all optional foreign key records from provided data
            biomedical_equipment: BiomedicalEquipment | None = None
            if request.biomedical_equipment:
                biomedical_equipment = BiomedicalEquipment.objects.create(
                    **request.biomedical_equipment
                )

            surgical: Surgical | None = None
            if request.surgical:
                surgical = Surgical.objects.create(**request.surgical)

            accessories_case: AccessoriesCase | None = None
            if request.accessories_case:
                accessories_case = AccessoriesCase.objects.create(
                    **request.accessories_case
                )

            respiratory: Respiratory | None = None
            if request.respiratory:
                respiratory = Respiratory.objects.create(**request.respiratory)

            immobilization_and_safety: ImmobilizationAndSafety | None = None
            if request.immobilization_and_safety:
                immobilization_and_safety = ImmobilizationAndSafety.objects.create(
                    **request.immobilization_and_safety
                )

            accessories: Accessories | None = None
            if request.accessories:
                accessories = Accessories.objects.create(**request.accessories)

            additionals: Additionals | None = None
            if request.additionals:
                additionals = Additionals.objects.create(**request.additionals)

            pediatric: Pediatric | None = None
            if request.pediatric:
                pediatric = Pediatric.objects.create(**request.pediatric)

            circulatory: Circulatory | None = None
            if request.circulatory:
                circulatory = Circulatory.objects.create(**request.circulatory)

            ambulance_kit: AmbulanceKit | None = None
            if request.ambulance_kit:
                ambulance_kit = AmbulanceKit.objects.create(**request.ambulance_kit)

            # Create inventory with all created foreign keys
            inventory: DailyMonthlyInventory = DailyMonthlyInventory.objects.create(
                system_user=user,
                ambulance=ambulance,
                biomedical_equipment=biomedical_equipment,
                surgical=surgical,
                accessories_case=accessories_case,
                respiratory=respiratory,
                immobilization_and_safety=immobilization_and_safety,
                accessories=accessories,
                additionals=additionals,
                pediatric=pediatric,
                circulatory=circulatory,
                ambulance_kit=ambulance_kit,
                date=request.date,
                observations=request.observations or "",
            )

            self.logger.info(
                f"Created inventory {inventory.pk} by user {user.username}"
            )
            return CreateInventoryResponse(inventory_id=inventory.pk)
        except Exception as e:
            self.logger.error(f"Error creating inventory: {str(e)}", exc_info=True)
            raise

    def get_inventory_by_id(self, inventory_id: int) -> InventoryDetailResponse | None:
        """
        Retrieve complete inventory details by ID.

        Args:
            inventory_id: ID of the DailyMonthlyInventory

        Returns:
            InventoryDetailResponse with all inventory information or None if not found
        """
        try:
            # Get inventory with all related objects
            inventory: DailyMonthlyInventory = (
                DailyMonthlyInventory.objects.select_related(
                    "system_user",
                    "ambulance",
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
                ).get(pk=inventory_id)
            )

            # Get person name from system_user
            person_name: str = ""
            system_user_id: int | None = None
            if inventory.system_user:
                user: User = inventory.system_user
                person_name = user.get_full_name() or user.username
                system_user_id = user.id

            # Helper function to serialize model to dict
            def model_to_dict(instance: Any) -> dict[str, Any] | None:
                if instance is None:
                    return None
                data: dict[str, Any] = {"id": instance.pk}
                for field in instance._meta.fields:
                    if field.name != "id":
                        value: Any = getattr(instance, field.name)
                        data[field.name] = value
                return data

            # Build detail response with complete related objects
            detail_response: InventoryDetailResponse = InventoryDetailResponse(
                inventory_id=inventory.pk,
                system_user_id=system_user_id,
                person_name=person_name,
                date=inventory.date,
                observations=inventory.observations,
                ambulance=model_to_dict(inventory.ambulance),
                biomedical_equipment=model_to_dict(inventory.biomedical_equipment),
                surgical=model_to_dict(inventory.surgical),
                accessories_case=model_to_dict(inventory.accessories_case),
                respiratory=model_to_dict(inventory.respiratory),
                immobilization_and_safety=model_to_dict(
                    inventory.immobilization_and_safety
                ),
                accessories=model_to_dict(inventory.accessories),
                additionals=model_to_dict(inventory.additionals),
                pediatric=model_to_dict(inventory.pediatric),
                circulatory=model_to_dict(inventory.circulatory),
                ambulance_kit=model_to_dict(inventory.ambulance_kit),
                created_at=inventory.created_at.isoformat(),
            )

            self.logger.info(f"Retrieved inventory detail for ID {inventory_id}")
            return detail_response

        except DailyMonthlyInventory.DoesNotExist:
            self.logger.warning(f"Inventory {inventory_id} not found")
            return None
        except Exception as e:
            self.logger.error(
                f"Error retrieving inventory {inventory_id}: {str(e)}", exc_info=True
            )
            raise
