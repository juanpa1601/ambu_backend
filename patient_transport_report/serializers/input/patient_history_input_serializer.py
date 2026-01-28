from rest_framework import serializers

# ==================== PATIENT HISTORY ====================
class PatientHistoryInputSerializer(serializers.Serializer):
    has_pathology = serializers.BooleanField(
        required=False, 
        default=False
    )
    pathology = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    has_allergies = serializers.BooleanField(
        required=False, 
        default=False
    )
    allergies = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    has_surgeries = serializers.BooleanField(
        required=False, 
        default=False
    )
    surgeries = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    has_medicines = serializers.BooleanField(
        required=False, 
        default=False
    )
    medicines = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    tobacco_use = serializers.BooleanField(
        required=False,
        default=False
    )
    substance_use = serializers.BooleanField(
        required=False, 
        default=False
    )
    alcohol_use = serializers.BooleanField(
        required=False, 
        default=False
    )
    other_history = serializers.CharField(
        required=False, 
        allow_blank=True
    )