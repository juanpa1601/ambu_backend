from rest_framework import serializers

# ==================== MEDICATION ADMINISTRATION ====================
class MedicationAdministrationInputSerializer(serializers.Serializer):
    oxygen = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    iv_fluids = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    admin_route_type = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    other_medication_details = serializers.CharField(
        required=False, 
        allow_blank=True
    )