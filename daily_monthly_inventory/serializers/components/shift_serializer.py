from rest_framework import serializers


class ShiftSerializer(serializers.Serializer):
    """
    Component serializer for Shift selection.
    Used to validate and handle shift selection in inventory operations.
    """

    id = serializers.IntegerField(
        required=True,
        allow_null=False,
        help_text="ID of the shift (day or night). Required field.",
    )

    def validate_id(self, value):
        """
        Validate that shift ID is not null or zero.
        """
        if value is None or value == 0:
            raise serializers.ValidationError("Debe seleccionar una jornada válida.")
        return value
