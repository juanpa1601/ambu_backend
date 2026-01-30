from rest_framework import serializers
from .glasgow_input_serializer import GlasgowInputSerializer

class PhysicalExamInputSerializer(serializers.Serializer):
    '''Input serializer for Physical Examination'''
    systolic: serializers.FloatField = serializers.FloatField(
        required=False, 
        allow_null=True
    )
    diastolic: serializers.FloatField = serializers.FloatField(
        required=False, 
        allow_null=True
    )
    map_pam: serializers.FloatField = serializers.FloatField(
        required=False, 
        allow_null=True
    )
    heart_rate: serializers.FloatField = serializers.FloatField(
        required=False, 
        allow_null=True
    )
    respiratory_rate: serializers.FloatField = serializers.FloatField(
        required=False, 
        allow_null=True
    )
    oxygen_saturation: serializers.FloatField = serializers.FloatField(
        required=False, 
        allow_null=True
    )
    temperature: serializers.FloatField = serializers.FloatField(
        required=False, 
        allow_null=True
    )
    blood_glucose: serializers.FloatField = serializers.FloatField(
        required=False, 
        allow_null=True
    )
    glasgow: GlasgowInputSerializer = GlasgowInputSerializer(
        required=False, 
        allow_null=True
    )