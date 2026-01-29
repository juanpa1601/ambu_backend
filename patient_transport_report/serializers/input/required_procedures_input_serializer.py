from rest_framework import serializers

# ==================== REQUIRED PROCEDURES ====================
class RequiredProceduresInputSerializer(serializers.Serializer):
    immobilization = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    stretcher_transfer = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    ambulance_transport = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    assessment = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    other_procedure_details = serializers.CharField(
        required=False, 
        allow_blank=True
    )