from rest_framework import serializers

class GlasgowInputSerializer(serializers.Serializer):
    '''Input serializer for Glasgow scale'''
    motor: serializers.IntegerField = serializers.IntegerField(
        min_value=1, 
        max_value=6, 
        required=False,
        allow_null=True 
    )
    motor_text: serializers.CharField = serializers.CharField(
        max_length=100, 
        required=False, 
        allow_blank=True
    )
    verbal: serializers.IntegerField = serializers.IntegerField(
        min_value=1, 
        max_value=5, 
        required=False,
        allow_null=True
    )
    verbal_text: serializers.CharField = serializers.CharField(
        max_length=100, 
        required=False, 
        allow_blank=True
    )
    eyes_opening: serializers.IntegerField = serializers.IntegerField(
        min_value=1, 
        max_value=4, 
        required=False,
        allow_null=True
    )
    eyes_opening_text: serializers.CharField = serializers.CharField(
        max_length=100, 
        required=False, 
        allow_blank=True
    )
    total: serializers.IntegerField = serializers.IntegerField(
        min_value=3, 
        max_value=15, 
        required=False,
        allow_null=True
    )