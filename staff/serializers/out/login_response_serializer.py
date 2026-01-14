from rest_framework import serializers

class LoginResponseSerializer(serializers.Serializer):
    '''Serializer for login response'''
    access_token: serializers.CharField = serializers.CharField()
    refresh_token: serializers.CharField = serializers.CharField()
    user_id: serializers.IntegerField = serializers.IntegerField()
    username: serializers.CharField = serializers.CharField()
    email: serializers.EmailField = serializers.EmailField()
    full_name: serializers.CharField = serializers.CharField()
    staff_type: serializers.CharField = serializers.CharField(allow_null=True)