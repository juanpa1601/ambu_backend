from rest_framework import serializers


class ShiftSerializer(serializers.Serializer):
    """
    Component serializer for Shift selection.
    Used to validate and handle shift selection in inventory operations.
    """

    id = serializers.IntegerField(
        required=True, help_text="ID of the shift (day or night)"
    )
