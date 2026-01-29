from rest_framework import serializers

# ==================== INSURANCE PROVIDER ====================
class InsuranceProviderInputSerializer(serializers.Serializer):
    coverage_type = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    provider_name = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    other_coverage_type = serializers.BooleanField(
        required=False, 
        default=False,
        allow_null=True
    )
    other_coverage_details = serializers.CharField(
        required=False, 
        allow_blank=True
    )