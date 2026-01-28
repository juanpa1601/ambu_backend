from rest_framework import serializers


class CreateInventorySerializer(serializers.Serializer):
    """Serializer para crear un nuevo inventario."""

    # Campos obligatorios
    date = serializers.DateField(required=True)
    ambulance_id = serializers.IntegerField(required=True)
    shift = serializers.DictField(required=True)  # {"id": int}

    # Campos opcionales del header
    support_staff = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    observations = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )

    # Secciones del inventario (opcionales)
    biomedical_equipment = serializers.DictField(
        required=False,
        allow_null=True,
    )
    surgical = serializers.DictField(
        required=False,
        allow_null=True,
    )
    accessories_case = serializers.DictField(
        required=False,
        allow_null=True,
    )
    respiratory = serializers.DictField(
        required=False,
        allow_null=True,
    )
    immobilization_and_safety = serializers.DictField(
        required=False,
        allow_null=True,
    )
    accessories = serializers.DictField(
        required=False,
        allow_null=True,
    )
    additionals = serializers.DictField(
        required=False,
        allow_null=True,
    )
    pediatric = serializers.DictField(
        required=False,
        allow_null=True,
    )
    circulatory = serializers.DictField(
        required=False,
        allow_null=True,
    )
    ambulance_kit = serializers.DictField(
        required=False,
        allow_null=True,
    )

    def validate(self, attrs):
        """Validar que campos requeridos estén presentes. 0 es un valor válido."""
        if not attrs.get("ambulance_id"):
            raise serializers.ValidationError(
                {"response": 'El campo de la "Ambulancia" es obligatorio.', "msg": -1}
            )

        if not attrs.get("date"):
            raise serializers.ValidationError(
                {"response": 'El campo de la "Fecha" es obligatorio.', "msg": -1}
            )

        if not attrs.get("shift"):
            raise serializers.ValidationError(
                {"response": 'El campo de la "Jornada" es obligatorio.', "msg": -1}
            )

        return attrs
