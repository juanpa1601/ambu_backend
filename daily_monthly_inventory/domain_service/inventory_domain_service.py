import logging
from typing import Any

from django.contrib.auth.models import User
from django.db.models.query import QuerySet
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
    Shift,
    Surgical,
)

from daily_monthly_inventory.types.dataclass import (
    AmbulanceListItem,
    AmbulanceListResponse,
    CreateInventoryRequest,
    CreateInventoryResponse,
    InventoryDetailResponse,
    InventoryListItem,
    InventoryListResponse,
    ShiftListItem,
    ShiftListResponse,
    UpdateInventoryRequest,
    UpdateInventoryResponse,
)


class InventoryDomainService:
    """Domain service for inventory-related operations."""

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

    def get_all_inventories(
        self,
        ambulance_id: int | None = None,
        month: int | None = None,
        year: int | None = None,
        day: int | None = None,
        system_user_id: int | None = None,
    ) -> InventoryListResponse:
        """
        Retrieve all daily/monthly inventories with basic information.

        Args:
            ambulance_id: Optional ambulance ID to filter by
            month: Optional month to filter by
            year: Optional year to filter by
            day: Optional day to filter by
            system_user_id: Optional user ID to filter by (for healthcare staff)

        Returns:
            InventoryListResponse with list of inventory items
        """
        try:
            # Query DailyMonthlyInventory with related system_user, ambulance and shift
            inventories_qs: QuerySet[DailyMonthlyInventory] = (
                DailyMonthlyInventory.objects.select_related(
                    "system_user", "ambulance", "shift"
                ).filter(is_deleted=False)
            )

            # Filter by user if specified (for healthcare staff)
            if system_user_id is not None:
                inventories_qs = inventories_qs.filter(system_user__id=system_user_id)
            
            if ambulance_id is not None:
                inventories_qs = inventories_qs.filter(ambulance__id=ambulance_id)
            if month is not None:
                inventories_qs = inventories_qs.filter(date__month=month)
            if year is not None:
                inventories_qs = inventories_qs.filter(date__year=year)
            if day is not None:
                inventories_qs = inventories_qs.filter(date__day=day)

            inventories: list[DailyMonthlyInventory] = list(inventories_qs.all())

            inventory_items: list[InventoryListItem] = []

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
                    is_completed=inventory.calculate_is_completed(),
                    shift=model_to_dict(inventory.shift),
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
                    f"User with ID {request.system_user_id} does not exist"
                )
                raise  # Re-raise Django's native exception

            # Resolve ambulance by ID (required)
            if not request.ambulance_id:
                self.logger.error(
                    "Se requiere el ID de la ambulancia para crear el inventario"
                )
                raise ValueError(
                    "Se requiere el ID de la ambulancia para crear el inventario"
                )

            try:
                ambulance: Ambulance = Ambulance.objects.get(id=request.ambulance_id)
            except Ambulance.DoesNotExist:
                self.logger.error(
                    f"Ambulance with ID {request.ambulance_id} does not exist"
                )
                raise  # Re-raise Django's native exception

            # Resolve shift by ID (optional)
            shift: Shift | None = None
            if request.shift_id:
                try:
                    shift = Shift.objects.get(id=request.shift_id)
                except Shift.DoesNotExist:
                    self.logger.error(
                        f"Shift with ID {request.shift_id} does not exist"
                    )
                    raise ValueError(f"La jornada con ID {request.shift_id} no existe")

            # Validate no duplicate inventory exists (same ambulance, day/month/year, and shift)
            if shift:
                existing_inventory: bool = DailyMonthlyInventory.objects.filter(
                    ambulance=ambulance,
                    date__year=request.date.year,
                    date__day=request.date.day,
                    date__month=request.date.month,
                    shift=shift,
                    is_deleted=False,
                ).exists()

                if existing_inventory:
                    self.logger.warning(
                        f"Duplicate inventory detected for ambulance {ambulance.id}, "
                        f"date {request.date.day}-{request.date.month}-{request.date.year}, shift {shift.name}"
                    )
                    raise ValueError(
                        f"Ya existe un inventario para la ambulancia {ambulance.mobile_number} "
                        f"en la fecha {request.date.strftime('%d/%m/%Y')} para la jornada de {shift.name}."
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
                shift=shift,
                support_staff=request.support_staff,
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
                observations=request.observations,
            )

            # Compute and persist is_completed
            inventory.is_completed = inventory.calculate_is_completed()
            inventory.save()

            self.logger.info(
                f"Created inventory {inventory.pk} by user {user.username}"
            )
            return CreateInventoryResponse(inventory_id=inventory.pk)
        except Exception as e:
            self.logger.error(f"Error creating inventory: {str(e)}", exc_info=True)
            raise

    def get_inventory_by_id(
        self,
        inventory_id: int,
    ) -> InventoryDetailResponse | None:
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
                shift=model_to_dict(inventory.shift),
                support_staff=inventory.support_staff,
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

    def update_inventory(
        self,
        request: UpdateInventoryRequest,
    ) -> UpdateInventoryResponse:
        """
        Update an existing inventory with new data.

        This method contains the domain logic for updating inventory and equipment.

        Args:
            request: UpdateInventoryRequest DTO with update data

        Returns:
            UpdateInventoryResponse with updated data

        Raises:
            DailyMonthlyInventory.DoesNotExist: If inventory not found
            Ambulance.DoesNotExist: If ambulance_id provided but not found
        """
        try:
            # Get the inventory with all related objects
            inventory: DailyMonthlyInventory = (
                DailyMonthlyInventory.objects.select_related(
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
                    "shift",
                ).get(id=request.inventory_id)
            )

            # Track which fields are being updated
            updated_fields: list[str] = []

            # Update simple fields
            if request.date is not None:
                inventory.date = request.date
                updated_fields.append("date")

            if request.observations is not None:
                inventory.observations = request.observations
                updated_fields.append("observations")

            # Update ambulance if provided
            if request.ambulance_id is not None:
                ambulance: Ambulance = Ambulance.objects.get(pk=request.ambulance_id)
                inventory.ambulance = ambulance
                updated_fields.append("ambulance")

            # Update shift if provided
            if request.shift_id is not None:
                shift: Shift = Shift.objects.get(pk=request.shift_id)
                inventory.shift = shift
                updated_fields.append("shift")

            # Update support_staff - always update to clear field when None is sent
            inventory.support_staff = request.support_staff if request.support_staff else ""
            updated_fields.append("support_staff")

            # Update equipment entities (create new or update existing)
            if request.biomedical_equipment is not None:
                if inventory.biomedical_equipment:
                    for key, value in request.biomedical_equipment.items():
                        setattr(inventory.biomedical_equipment, key, value)
                    inventory.biomedical_equipment.save()
                else:
                    inventory.biomedical_equipment = BiomedicalEquipment.objects.create(
                        **request.biomedical_equipment
                    )
                updated_fields.append("biomedical_equipment")

            if request.surgical is not None:
                if inventory.surgical:
                    for key, value in request.surgical.items():
                        setattr(inventory.surgical, key, value)
                    inventory.surgical.save()
                else:
                    inventory.surgical = Surgical.objects.create(**request.surgical)
                updated_fields.append("surgical")

            if request.accessories_case is not None:
                if inventory.accessories_case:
                    for key, value in request.accessories_case.items():
                        setattr(inventory.accessories_case, key, value)
                    inventory.accessories_case.save()
                else:
                    inventory.accessories_case = AccessoriesCase.objects.create(
                        **request.accessories_case
                    )
                updated_fields.append("accessories_case")

            if request.respiratory is not None:
                if inventory.respiratory:
                    for key, value in request.respiratory.items():
                        setattr(inventory.respiratory, key, value)
                    inventory.respiratory.save()
                else:
                    inventory.respiratory = Respiratory.objects.create(
                        **request.respiratory
                    )
                updated_fields.append("respiratory")

            if request.immobilization_and_safety is not None:
                if inventory.immobilization_and_safety:
                    for key, value in request.immobilization_and_safety.items():
                        setattr(inventory.immobilization_and_safety, key, value)
                    inventory.immobilization_and_safety.save()
                else:
                    inventory.immobilization_and_safety = (
                        ImmobilizationAndSafety.objects.create(
                            **request.immobilization_and_safety
                        )
                    )
                updated_fields.append("immobilization_and_safety")

            if request.accessories is not None:
                if inventory.accessories:
                    for key, value in request.accessories.items():
                        setattr(inventory.accessories, key, value)
                    inventory.accessories.save()
                else:
                    inventory.accessories = Accessories.objects.create(
                        **request.accessories
                    )
                updated_fields.append("accessories")

            if request.additionals is not None:
                if inventory.additionals:
                    for key, value in request.additionals.items():
                        setattr(inventory.additionals, key, value)
                    inventory.additionals.save()
                else:
                    inventory.additionals = Additionals.objects.create(
                        **request.additionals
                    )
                updated_fields.append("additionals")

            if request.pediatric is not None:
                if inventory.pediatric:
                    for key, value in request.pediatric.items():
                        setattr(inventory.pediatric, key, value)
                    inventory.pediatric.save()
                else:
                    inventory.pediatric = Pediatric.objects.create(**request.pediatric)
                updated_fields.append("pediatric")

            if request.circulatory is not None:
                if inventory.circulatory:
                    for key, value in request.circulatory.items():
                        setattr(inventory.circulatory, key, value)
                    inventory.circulatory.save()
                else:
                    inventory.circulatory = Circulatory.objects.create(
                        **request.circulatory
                    )
                updated_fields.append("circulatory")

            if request.ambulance_kit is not None:
                if inventory.ambulance_kit:
                    for key, value in request.ambulance_kit.items():
                        setattr(inventory.ambulance_kit, key, value)
                    inventory.ambulance_kit.save()
                else:
                    inventory.ambulance_kit = AmbulanceKit.objects.create(
                        **request.ambulance_kit
                    )
                updated_fields.append("ambulance_kit")

            # Save inventory
            inventory.save()

            # Recompute and persist is_completed after saving other changes
            inventory.is_completed = inventory.calculate_is_completed()
            inventory.save()

            self.logger.info(
                f"Updated inventory {inventory.pk}. Fields updated: {', '.join(updated_fields)}"
            )

            return UpdateInventoryResponse(
                inventory_id=inventory.pk,
                date=inventory.date.isoformat(),
                observations=inventory.observations,
                fields_updated=updated_fields,
            )

        except Exception as e:
            self.logger.error(
                f"Error updating inventory {request.inventory_id}: {str(e)}",
                exc_info=True,
            )
            raise

    def get_all_shifts(self) -> ShiftListResponse:
        """
        Retrieve all available shifts from the database.

        Returns:
            ShiftListResponse with list of shift items
        """
        try:
            shifts: list[Shift] = Shift.objects.all()

            shift_items: list[ShiftListItem] = []
            for shift in shifts:
                shift_item: ShiftListItem = ShiftListItem(
                    id=shift.pk,
                    name=shift.name,
                )
                shift_items.append(shift_item)

            self.logger.info(f"Retrieved {len(shift_items)} shifts")
            return ShiftListResponse(shifts=shift_items, total_count=len(shift_items))

        except Exception as e:
            self.logger.error(f"Error retrieving shifts: {str(e)}", exc_info=True)
            raise

    def get_all_ambulances(self) -> AmbulanceListResponse:
        """
        Retrieve all active ambulances from the database.

        Returns:
            AmbulanceListResponse with list of ambulance items
        """
        try:
            ambulances: list[Ambulance] = list(
                Ambulance.objects.filter(is_active=True).order_by("mobile_number")
            )

            ambulance_items: list[AmbulanceListItem] = []
            for ambulance in ambulances:
                display_name: str = (
                    f"Móvil {ambulance.mobile_number} - {ambulance.license_plate}"
                    if ambulance.license_plate
                    else f"Móvil {ambulance.mobile_number}"
                )

                ambulance_item: AmbulanceListItem = AmbulanceListItem(
                    id=ambulance.pk,
                    mobile_number=ambulance.mobile_number,
                    license_plate=ambulance.license_plate or "",
                    display_name=display_name,
                )
                ambulance_items.append(ambulance_item)

            self.logger.info(f"Retrieved {len(ambulance_items)} ambulances")
            return AmbulanceListResponse(
                ambulances=ambulance_items, total_count=len(ambulance_items)
            )

        except Exception as e:
            self.logger.error(f"Error retrieving ambulances: {str(e)}", exc_info=True)
            raise
