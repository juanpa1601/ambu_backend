from rest_framework import serializers

class EntityInputSerializer(serializers.Serializer):
    '''Input serializer for Outgoing/Receiving Entity'''
    name: serializers.CharField = serializers.CharField(
        max_length=200, 
        required=False, 
        allow_blank=True
    )
    document: serializers.CharField = serializers.CharField(
        max_length=100, 
        required=False, 
        allow_blank=True
    )
    staff_title: serializers.CharField = serializers.CharField(
        max_length=100, 
        required=False, 
        allow_blank=True
    )