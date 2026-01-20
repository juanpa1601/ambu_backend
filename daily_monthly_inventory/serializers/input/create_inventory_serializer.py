from rest_framework import serializers


class CreateInventorySerializer(serializers.Serializer):
    date = serializers.DateField()
    ambulance_id = serializers.IntegerField(required=False, allow_null=True)
    biomedical_equipment = serializers.DictField(required=False, allow_null=True)
    surgical = serializers.DictField(required=False, allow_null=True)
    accessories_case = serializers.DictField(required=False, allow_null=True)
    respiratory = serializers.DictField(required=False, allow_null=True)
    immobilization_and_safety = serializers.DictField(required=False, allow_null=True)
    accessories = serializers.DictField(required=False, allow_null=True)
    additionals = serializers.DictField(required=False, allow_null=True)
    pediatric = serializers.DictField(required=False, allow_null=True)
    circulatory = serializers.DictField(required=False, allow_null=True)
    ambulance_kit = serializers.DictField(required=False, allow_null=True)
    observations = serializers.CharField(required=False, allow_blank=True, default='')
