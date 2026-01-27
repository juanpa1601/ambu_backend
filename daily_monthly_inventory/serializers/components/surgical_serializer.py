from rest_framework import serializers


class SurgicalSerializer(serializers.Serializer):
    """
    Component serializer for Surgical model.
    Validates all fields with proper types and constraints matching the model.
    """

    surgical_soap = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Surgical soap quantity"
    )
    antiseptic_soap = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Antiseptic soap quantity"
    )
    alcohol_120ml = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Alcohol 120ml quantity"
    )
    safety_goggles = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Safety goggles quantity"
    )
    kidney_dish = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Kidney dish quantity"
    )
    magill_forceps = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Magill forceps quantity"
    )
    thermal_blanket = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Thermal blanket quantity"
    )
    triangular_bandage = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Triangular bandage quantity",
    )
    sterile_surgical_gauze = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=20,
        help_text="Sterile surgical gauze quantity",
    )
    gauze_compress = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Gauze compress quantity"
    )
    elastic_bandage = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Elastic bandage quantity"
    )
    gauze_bandage = serializers.IntegerField(
        required=False, min_value=0, max_value=20, help_text="Gauze bandage quantity"
    )
    cotton_bundle = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Cotton bundle quantity"
    )
    sterile_gloves = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Sterile gloves quantity"
    )
