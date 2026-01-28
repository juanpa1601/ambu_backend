from rest_framework import serializers


class AdditionalsSerializer(serializers.Serializer):
    """
    Component serializer for Additionals model.
    Validates all fields with proper types and constraints matching the model.
    """

    tablet = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Tablet quantity",
    )
    charger = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Charger quantity",
    )
    data_clipboard_board = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Data clipboard board quantity",
    )
    medical_record_forms = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=20,
        allow_null=True,
        help_text="Medical record forms quantity",
    )
    cleaning_log_form = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Cleaning log form quantity",
    )
    temperature_log_form = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Temperature log form quantity",
    )
    artificial_tears = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Artificial tears quantity",
    )
    observations_comments = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        allow_null=True,
        help_text="Observations and comments",
    )
