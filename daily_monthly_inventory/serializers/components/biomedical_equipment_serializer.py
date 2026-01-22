from rest_framework import serializers


class BiomedicalEquipmentSerializer(serializers.Serializer):
    """
    Component serializer for BiomedicalEquipment model.
    Validates all fields with proper types and constraints matching the model.
    """

    monitor = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Monitor quantity"
    )
    aed = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="AED quantity"
    )
    adult_pads = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Adult pads quantity"
    )
    pediatric_pads = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Pediatric pads quantity"
    )
    aspirator = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Aspirator quantity"
    )
    flowmeter = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Flowmeter quantity"
    )
    glucometer = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Glucometer quantity"
    )
    pulse_oximeter = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Pulse oximeter quantity"
    )
    central_oxygen = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Central oxygen quantity"
    )
    portable_oxygen_1 = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Portable oxygen #1 quantity",
    )
    portable_oxygen_2 = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Portable oxygen #2 quantity",
    )
    spencer_scissors = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Spencer scissors quantity"
    )
    search_light = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Search light quantity"
    )
    reflex_hammer = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Reflex hammer quantity"
    )
