from rest_framework import serializers

class ComplicationsInputSerializer(serializers.Serializer):
    '''Input serializer for Complications'''
    description_complication: serializers.CharField = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    register_code: serializers.BooleanField = serializers.BooleanField(
        required=False,
        allow_null=True
    )
    code: serializers.CharField = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    record_waiting_time: serializers.BooleanField = serializers.BooleanField(
        required=False,
        allow_null=True
    )
    waiting_time: serializers.CharField = serializers.CharField(
        required=False, 
        allow_null=True
    )
    time_code: serializers.CharField = serializers.CharField(
        required=False, 
        allow_blank=True
    )