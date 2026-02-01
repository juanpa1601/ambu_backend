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
        For new inventories: require shift and ambulance fields.
        """
        inventory_id = data.get('inventory_id')
        
        # If creating new inventory (inventory_id is None), require shift and ambulance
        if inventory_id is None:
            # Validate shift is present
            if 'shift' not in data or data.get('shift') is None:
                raise serializers.ValidationError({
                    'shift': 'La jornada es obligatoria para crear un inventario.'
                })
            # Validate shift has an id
            shift_data = data.get('shift')
            if isinstance(shift_data, dict) and not shift_data.get('id'):
                raise serializers.ValidationError({
                    'shift': 'Debe seleccionar una jornada válida.'
                })
            
            # Validate ambulance is present
            if 'ambulance_id' not in data or data.get('ambulance_id') is None:
                raise serializers.ValidationError({
                    'ambulance_id': 'La ambulancia es obligatoria para crear un inventario.'
                })
            # Validate ambulance_id is not zero or negative
            ambulance_id = data.get('ambulance_id')
            if isinstance(ambulance_id, int) and ambulance_id <= 0:
                raise serializers.ValidationError({
                    'ambulance_id': 'Debe seleccionar una ambulancia válida.'
                })
            
            return data
            
        # For updates, ensure at least one field besides inventory_id is provided
        fields_without_id = {k: v for k, v in data.items() if k != 'inventory_id'}
        if not fields_without_id:
            raise serializers.ValidationError(
                "Debe proporcionar al menos un campo para actualizar."
            )
        return data
