from rest_framework import serializers

# ==================== REQUIRED PROCEDURES ====================
class RequiredProceduresInputSerializer(serializers.Serializer):
    immobilization = serializers.BooleanField(
        required=False, 
        default=False
    )
    stretcher_transfer = serializers.BooleanField(
        required=False, 
        default=False
    )
    ambulance_transport = serializers.BooleanField(
        required=False, 
        default=False
    )
    assessment = serializers.BooleanField(
        required=False, 
        default=False
    )
    other_procedure_details = serializers.CharField(
        required=False, 
        allow_blank=True
    )