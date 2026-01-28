from rest_framework import serializers


class RespiratorySerializer(serializers.Serializer):
    """
    Component serializer for Respiratory model.
    Validates all fields with proper types and constraints matching the model.
    """

    simple_humidifier_jar = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Simple humidifier jar quantity",
    )
    venturi_humidifier_jar = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Venturi humidifier jar quantity",
    )
    laryngeal_mask_4 = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Laryngeal mask #4 quantity",
    )
    laryngeal_mask_5 = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Laryngeal mask #5 quantity",
    )
    adult_nasal_cannula = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Adult nasal cannula quantity",
    )
    adult_simple_mask = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Adult simple mask quantity",
    )
    adult_non_rebreather_mask = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Adult non-rebreather mask quantity",
    )
    adult_venturi_system = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Adult venturi system quantity",
    )
    adult_nebulizer_kit = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Adult nebulizer kit quantity",
    )
    oropharyngeal_airway_3 = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Oropharyngeal airway #3 quantity",
    )
    oropharyngeal_airway_4 = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Oropharyngeal airway #4 quantity",
    )
    oropharyngeal_airway_5 = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Oropharyngeal airway #5 quantity",
    )
    o2_connecting_tube = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="O2 connecting tube quantity",
    )
    adult_bvm_bag_valve_mask = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Adult BVM bag valve mask quantity",
    )
    yankauer_suction_tip = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Yankauer suction tip quantity",
    )
    adult_spacer_chamber = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Adult spacer chamber quantity",
    )
    suction_tubing = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Suction tubing quantity",
    )
    suction_catheter = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        allow_null=True,
        help_text="Suction catheter quantity",
    )
