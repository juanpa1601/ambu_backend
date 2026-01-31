from rest_framework import serializers


class BiomedicalEquipmentSerializer(serializers.Serializer):
    """
    Component serializer for BiomedicalEquipment model.
    Validates all fields with proper types and constraints matching the model.
    """

    monitor = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Monitor quantity",
        allow_null=True,
    )
    aed = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="AED quantity",
        allow_null=True,
    )
    adult_pads = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Adult pads quantity",
        allow_null=True,
    )
    pediatric_pads = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Pediatric pads quantity",
        allow_null=True,
    )
    aspirator = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Aspirator quantity",
        allow_null=True,
    )
    flowmeter = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Flowmeter quantity",
        allow_null=True,
    )
    glucometer = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Glucometer quantity",
        allow_null=True,
    )
    pulse_oximeter = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Pulse oximeter quantity",
        allow_null=True,
    )
    central_oxygen = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Central oxygen quantity",
        allow_null=True,
    )
    portable_oxygen_1 = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Portable oxygen #1 quantity",
        allow_null=True,
    )
    portable_oxygen_2 = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Portable oxygen #2 quantity",
        allow_null=True,
    )
    spencer_scissors = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Spencer scissors quantity",
        allow_null=True,
    )
    search_light = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Search light quantity",
        allow_null=True,
    )
    reflex_hammer = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Reflex hammer quantity",
        allow_null=True,
    )
