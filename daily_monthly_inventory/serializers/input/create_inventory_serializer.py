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


class CreateInventorySerializer(serializers.Serializer):
    """
    Input serializer for creating a new inventory.
    Uses component serializers for proper field-level validation.

    All category fields are optional to allow partial inventory creation.
    The 'date' field is required.
    """

    date = serializers.DateField(required=True, help_text="Date of the inventory")
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
        default="",
        help_text="General observations and comments about the inventory",
    )
