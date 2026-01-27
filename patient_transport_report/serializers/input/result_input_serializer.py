from rest_framework import serializers

class ResultInputSerializer(serializers.Serializer):
    '''Input serializer for Result'''
    no_vital_signs: serializers.BooleanField = serializers.BooleanField(required=False)
    denies_transportation: serializers.BooleanField = serializers.BooleanField(required=False)
    schelud_transfer: serializers.BooleanField = serializers.BooleanField(required=False)