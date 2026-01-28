from rest_framework import serializers


class AmbulanceKitSerializer(serializers.Serializer):
    """
    Component serializer for AmbulanceKit model.
    Validates all fields with proper types and constraints matching the model.
    """

    trauma_shears = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Trauma shears quantity",
    )
    sterile_gauze_kit = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=20,
        allow_null=True,
        help_text="Sterile gauze kit quantity",
    )
    iv_tourniquet = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="IV tourniquet quantity",
    )
    hemorrhage_control_tourniquet = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Hemorrhage control tourniquet quantity",
    )
    medical_penlight = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Medical penlight quantity",
    )
    micropore_tape = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Micropore tape quantity",
    )
    adhesive_tape = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Adhesive tape quantity",
    )
    surgical_masks = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=20,
        allow_null=True,
        help_text="Surgical masks quantity",
    )
    n95_masks = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=20,
        allow_null=True,
        help_text="N95 masks quantity",
    )
    alcohol_pads = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=20,
        allow_null=True,
        help_text="Alcohol pads quantity",
    )
    eye_patches = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=20,
        allow_null=True,
        help_text="Eye patches quantity",
    )
    tongue_depressors = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=20,
        allow_null=True,
        help_text="Tongue depressors quantity",
    )
    cotton_tipped_applicators = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=20,
        allow_null=True,
        help_text="Cotton-tipped applicators quantity",
    )
    clinical_thermometer = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Clinical thermometer quantity",
    )
    sanitary_pads = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=20,
        allow_null=True,
        help_text="Sanitary pads quantity",
    )
