from rest_framework import serializers

class TreatmentInputSerializer(serializers.Serializer):
    '''Input serializer for Treatment'''
    monitors_vital_signs: serializers.BooleanField = serializers.BooleanField(required=False)
    oxygen: serializers.BooleanField = serializers.BooleanField(required=False)
    liter_minute: serializers.FloatField = serializers.FloatField(
        required=False,
        allow_null=True
    )
    nasal_cannula: serializers.BooleanField = serializers.BooleanField(required=False)
    simple_face_mask: serializers.BooleanField = serializers.BooleanField(required=False)
    non_rebreather_mask: serializers.BooleanField = serializers.BooleanField(required=False)