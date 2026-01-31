from rest_framework import serializers


class AccessoriesSerializer(serializers.Serializer):
    """
    Component serializer for Accessories model.
    Validates all fields with proper types and constraints matching the model.
    """

    eucida_advanced_disinfectant = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Eucida advanced disinfectant quantity",
    )
    wypall_towels = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=20,
        allow_null=True,
        help_text="Wypall towels quantity",
    )
    patient_blanket = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Patient blanket quantity",
    )
    stretcher_sheet = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=20,
        allow_null=True,
        help_text="Stretcher sheet quantity",
    )
    gloves_boxes = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Gloves boxes quantity",
    )
    chemical_attack_kit_forms = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Chemical attack kit forms quantity",
    )
    chemical_attack_kit_ph_tape = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Chemical attack kit pH tape quantity",
    )
    adult_pediatric_stethoscope = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Adult/pediatric stethoscope quantity",
    )
    adult_sphygmomanometer = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Adult sphygmomanometer quantity",
    )
    white_waste_bags = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=20,
        allow_null=True,
        help_text="White waste bags quantity",
    )
    red_biohazard_bags = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=20,
        allow_null=True,
        help_text="Red biohazard bags quantity",
    )
    clean_gauze_pack = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Clean gauze pack quantity",
    )
    red_biohazard_container = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Red biohazard container quantity",
    )
    white_waste_container = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="White waste container quantity",
    )
    wheelchair = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Wheelchair quantity",
    )
    short_spinal_board = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Short spinal board quantity",
    )
    male_urinal = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Male urinal quantity",
    )
    female_urinal = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Female urinal quantity",
    )
    thermo_hygrometer = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Thermo hygrometer quantity",
    )
