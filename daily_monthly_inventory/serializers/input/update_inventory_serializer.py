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
)


class UpdateInventorySerializer(serializers.Serializer):
    """
    Input serializer for updating an existing inventory (PATCH endpoint).
    Uses component serializers for proper field-level validation.

    All fields are optional to support partial updates.
    At least one field must be provided.
    """

    date = serializers.DateField(required=False, help_text="Date of the inventory")
    ambulance_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="ID of the ambulance this inventory belongs to",
    )

    # Nested category serializers with proper validation
    biomedical_equipment = BiomedicalEquipmentSerializer(
        required=False, allow_null=True
    )
    surgical = SurgicalSerializer(required=False, allow_null=True)
    accessories_case = AccessoriesCaseSerializer(required=False, allow_null=True)
    respiratory = RespiratorySerializer(required=False, allow_null=True)
    immobilization_and_safety = ImmobilizationAndSafetySerializer(
        required=False, allow_null=True
    )
    accessories = AccessoriesSerializer(required=False, allow_null=True)
    additionals = AdditionalsSerializer(required=False, allow_null=True)
    pediatric = PediatricSerializer(required=False, allow_null=True)
    circulatory = CirculatorySerializer(required=False, allow_null=True)
    ambulance_kit = AmbulanceKitSerializer(required=False, allow_null=True)

    observations = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="General observations and comments about the inventory",
    )

    def validate(self, data):
        """
        Validate that at least one field is provided for update.
        """
        if not data:
            raise serializers.ValidationError(
                "Debe proporcionar al menos un campo para actualizar."
            )
        return data
