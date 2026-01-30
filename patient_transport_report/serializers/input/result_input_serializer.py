from rest_framework import serializers

class ResultInputSerializer(serializers.Serializer):
    '''Input serializer for Result'''
    no_vital_signs: serializers.BooleanField = serializers.BooleanField(
        required=False,
        allow_null=True
    )
    denies_transportation: serializers.BooleanField = serializers.BooleanField(
        required=False,
        allow_null=True
    )
    schelud_transfer: serializers.BooleanField = serializers.BooleanField(
        required=False,
        allow_null=True
    )