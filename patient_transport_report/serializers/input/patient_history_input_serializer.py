from rest_framework import serializers

# ==================== PATIENT HISTORY ====================
class PatientHistoryInputSerializer(serializers.Serializer):
    has_pathology = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    pathology = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    has_allergies = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    allergies = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    has_surgeries = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    surgeries = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    has_medicines = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    medicines = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    tobacco_use = serializers.BooleanField(
        required=False,
        default=False,
        allow_null=True
    )
    substance_use = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    alcohol_use = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    other_history = serializers.CharField(
        required=False, 
        allow_blank=True
    )