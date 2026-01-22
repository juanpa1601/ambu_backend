from rest_framework import serializers


class PediatricSerializer(serializers.Serializer):
    """
    Component serializer for Pediatric model.
    Validates all fields with proper types and constraints matching the model.
    """

    pediatric_nasal_cannula = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Pediatric nasal cannula quantity",
    )
    pediatric_simple_mask = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Pediatric simple mask quantity",
    )
    pediatric_non_rebreather_mask = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Pediatric non-rebreather mask quantity",
    )
    pediatric_venturi_system = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Pediatric venturi system quantity",
    )
    pediatric_nebulizer_kit = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Pediatric nebulizer kit quantity",
    )
    pediatric_bvm_bag_valve_mask = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Pediatric BVM bag valve mask quantity",
    )
    suction_bulb_aspirator = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Suction bulb aspirator quantity",
    )
    pediatric_sphygmomanometer = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Pediatric sphygmomanometer quantity",
    )
    oropharyngeal_airway_0 = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Oropharyngeal airway #0 quantity",
    )
    oropharyngeal_airway_1 = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Oropharyngeal airway #1 quantity",
    )
    oropharyngeal_airway_2 = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Oropharyngeal airway #2 quantity",
    )
    laryngeal_mask_1_5 = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Laryngeal mask 1.5 quantity",
    )
    laryngeal_mask_2 = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Laryngeal mask #2 quantity",
    )
    laryngeal_mask_3 = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Laryngeal mask #3 quantity",
    )
    umbilical_cord_clamp = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10,
        help_text="Umbilical cord clamp quantity",
    )
