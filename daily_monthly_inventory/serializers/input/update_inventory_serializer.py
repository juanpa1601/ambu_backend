from rest_framework import serializers


class UpdateInventorySerializer(serializers.Serializer):
    """
    Serializer for updating inventory information.
    All fields are optional - only provided fields will be updated.
    """

    date = serializers.DateField(required=False, allow_null=True)
    ambulance_id = serializers.IntegerField(required=False, allow_null=True)
    biomedical_equipment = serializers.DictField(required=False, allow_null=True)
    surgical = serializers.DictField(required=False, allow_null=True)
    accessories_case = serializers.DictField(required=False, allow_null=True)
    respiratory = serializers.DictField(required=False, allow_null=True)
    immobilization_and_safety = serializers.DictField(required=False, allow_null=True)
    accessories = serializers.DictField(required=False, allow_null=True)
    additionals = serializers.DictField(required=False, allow_null=True)
    pediatric = serializers.DictField(required=False, allow_null=True)
    circulatory = serializers.DictField(required=False, allow_null=True)
    ambulance_kit = serializers.DictField(required=False, allow_null=True)
    observations = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
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
