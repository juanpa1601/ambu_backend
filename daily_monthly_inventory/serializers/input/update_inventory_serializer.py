from rest_framework import serializers
from daily_monthly_inventory.serializers.components import (
    AdditionalsSerializer,
    SurgicalSerializer,
    RespiratorySerializer,
    BiomedicalEquipmentSerializer,
    AccessoriesSerializer,
    ImmobilizationAndSafetySerializer,
    PediatricSerializer,
    CirculatorySerializer,
    AmbulanceKitSerializer,
    AccessoriesCaseSerializer,
    ShiftSerializer,
)


class UpdateInventorySerializer(serializers.Serializer):
    """
    Input serializer for updating an existing inventory (PATCH endpoint).
    Also used for save_inventory endpoint which handles both create and update.
    Uses component serializers for proper field-level validation.

    All fields are optional to support partial updates.
    At least one field must be provided.
    """

    inventory_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="ID of the inventory to update. If null, a new inventory will be created.",
    )
    date = serializers.DateField(
        required=False,
        help_text="Date of the inventory",
    )
    ambulance_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="ID of the ambulance this inventory belongs to",
    )
    shift = ShiftSerializer(
        required=False,
        allow_null=True,
        help_text="Shift information (day or night)",
    )
    support_staff = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="Names of support staff who participated in the inventory",
    )

    # Nested category serializers with proper validation
    biomedical_equipment = BiomedicalEquipmentSerializer(
        required=False,
        allow_null=True,
    )
    surgical = SurgicalSerializer(
        required=False,
        allow_null=True,
    )
    accessories_case = AccessoriesCaseSerializer(
        required=False,
        allow_null=True,
    )
    respiratory = RespiratorySerializer(
        required=False,
        allow_null=True,
    )
    immobilization_and_safety = ImmobilizationAndSafetySerializer(
        required=False,
        allow_null=True,
    )
    accessories = AccessoriesSerializer(
        required=False,
        allow_null=True,
    )
    additionals = AdditionalsSerializer(
        required=False,
        allow_null=True,
    )
    pediatric = PediatricSerializer(
        required=False,
        allow_null=True,
    )
    circulatory = CirculatorySerializer(
        required=False,
        allow_null=True,
    )
    ambulance_kit = AmbulanceKitSerializer(
        required=False,
        allow_null=True,
    )

    observations = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="General observations and comments about the inventory",
    )

    def validate(self, data):
        """
        Validate that at least one field is provided for update.
        For save_inventory endpoint: skip validation if inventory_id is None (create mode).
        """
        inventory_id = data.get('inventory_id')
        
        # If creating new inventory (inventory_id is None), skip the "at least one field" check
        if inventory_id is None:
            return data
            
        # For updates, ensure at least one field besides inventory_id is provided
        fields_without_id = {k: v for k, v in data.items() if k != 'inventory_id'}
        if not fields_without_id:
            raise serializers.ValidationError(
                "Debe proporcionar al menos un campo para actualizar."
            )
        return data
