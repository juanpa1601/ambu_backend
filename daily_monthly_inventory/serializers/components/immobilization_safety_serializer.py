from rest_framework import serializers


class ImmobilizationAndSafetySerializer(serializers.Serializer):
    """
    Component serializer for ImmobilizationAndSafety model.
    Validates all fields with proper types and constraints matching the model.
    """

    adult_cervical_collar = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Adult cervical collar quantity",
    )
    pediatric_cervical_collar = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Pediatric cervical collar quantity",
    )
    adult_immobilization_kit = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Adult immobilization kit quantity",
    )
    pediatric_immobilization_kit = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Pediatric immobilization kit quantity",
    )
    benziral_spill_kit = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Benziral spill kit quantity",
    )
    west_solidifier_spill_kit = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="West solidifier spill kit quantity",
    )
    stretcher_side_rails = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Stretcher side rails quantity",
    )
    stretcher_harness_straps = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Stretcher harness straps quantity",
    )
    ambumedic_umbrella = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Ambumedic umbrella quantity",
    )
    safety_vests = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Safety vests quantity",
    )
