from rest_framework import serializers

class CompanionInputSerializer(serializers.Serializer):
    '''Input serializer for Companion'''
    name: serializers.CharField = serializers.CharField(
        max_length=200, 
        required=False, 
        allow_blank=True
    )
    identification_type: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    identification_number: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    phone_number: serializers.CharField = serializers.CharField(
        max_length=20, 
        required=False, 
        allow_blank=True
    )
    kindship: serializers.CharField = serializers.CharField(
        max_length=100, 
        required=False, 
        allow_blank=True
    )