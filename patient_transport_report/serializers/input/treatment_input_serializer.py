from rest_framework import serializers

class TreatmentInputSerializer(serializers.Serializer):
    '''Input serializer for Treatment'''
    monitors_vital_signs: serializers.BooleanField = serializers.BooleanField(
        required=False,
        allow_null=True
    )
    oxygen: serializers.BooleanField = serializers.BooleanField(
        required=False,
        allow_null=True
    )
    liter_minute: serializers.FloatField = serializers.FloatField(
        required=False,
        allow_null=True
    )
    nasal_cannula: serializers.BooleanField = serializers.BooleanField(
        required=False,
        allow_null=True
    )
    simple_face_mask: serializers.BooleanField = serializers.BooleanField(
        required=False,
        allow_null=True
    )
    non_rebreather_mask: serializers.BooleanField = serializers.BooleanField(
        required=False,
        allow_null=True
    )