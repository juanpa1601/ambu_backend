from rest_framework import serializers


class AccessoriesCaseSerializer(serializers.Serializer):
    """
    Component serializer for AccessoriesCase model.
    Validates all fields with proper types and constraints matching the model.
    """

    adult_bp_cuff = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Adult BP cuff quantity",
    )
    pediatric_bp_cuff = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Pediatric BP cuff quantity",
        allow_null=True,
    )
    adult_spo2_sensor = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Adult SPO2 sensor quantity",
        allow_null=True,
    )
    pediatric_spo2_sensor = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Pediatric SPO2 sensor quantity",
        allow_null=True,
    )
    carsioscope_cables = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Cardiac SPO2 sensor quantity",
    )
    temperature_sensor = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Temperature sensor quantity",
    )
