from rest_framework import serializers


class CirculatorySerializer(serializers.Serializer):
    """
    Component serializer for Circulatory model.
    Validates all fields with proper types and constraints matching the model.
    """

    saline_solution_09_500cc = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=20,
        help_text="Saline solution 0.9% 500cc quantity",
    )
    dextrose_5_percent = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Dextrose 5% quantity"
    )
    dextrose_10_percent = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Dextrose 10% quantity"
    )
    hartmann_lactate_solution = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=20,
        help_text="Hartmann lactate solution quantity",
    )
    macro_drip_set = serializers.IntegerField(
        required=False, min_value=0, max_value=20, help_text="Macro drip set quantity"
    )
    micro_drip_set = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Micro drip set quantity"
    )
    sterile_water = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Sterile water quantity"
    )
    syringe_1cc = serializers.IntegerField(
        required=False, min_value=0, max_value=20, help_text="Syringe 1cc quantity"
    )
    syringe_3cc = serializers.IntegerField(
        required=False, min_value=0, max_value=20, help_text="Syringe 3cc quantity"
    )
    syringe_5cc = serializers.IntegerField(
        required=False, min_value=0, max_value=20, help_text="Syringe 5cc quantity"
    )
    syringe_10cc = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Syringe 10cc quantity"
    )
    syringe_20cc = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Syringe 20cc quantity"
    )
    syringe_50cc = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Syringe 50cc quantity"
    )
    iv_catheter_14g = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="IV catheter 14G quantity"
    )
    iv_catheter_16g = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="IV catheter 16G quantity"
    )
    iv_catheter_18g = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="IV catheter 18G quantity"
    )
    iv_catheter_20g = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="IV catheter 20G quantity"
    )
    iv_catheter_22g = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="IV catheter 22G quantity"
    )
    iv_catheter_24g = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="IV catheter 24G quantity"
    )
    scalp_vein_set_21g = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Scalp vein set 21G quantity",
    )
    scalp_vein_set_22g = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Scalp vein set 22G quantity",
    )
    scalp_vein_set_23g = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Scalp vein set 23G quantity",
    )
    sharps_container = serializers.IntegerField(
        required=False, min_value=0, max_value=10, help_text="Sharps container quantity"
    )
