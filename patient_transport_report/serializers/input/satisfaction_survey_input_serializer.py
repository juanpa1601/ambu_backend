from rest_framework import serializers

class SatisfactionSurveyInputSerializer(serializers.Serializer):
    '''Input serializer for Satisfaction Survey'''
    ambulance_request_ease: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    phone_support_quality: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    service_punctuality: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    clear_info_provided: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    staff_appearance: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    ambulance_cleanliness: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    driving_quality: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    return_trip_timeliness: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    safety_and_reassurance: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    staff_empathy: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    overall_satisfaction: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    would_recommend: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    comments: serializers.CharField = serializers.CharField(
        required=False, 
        allow_blank=True
    )
    respondent_can_sign: serializers.BooleanField = serializers.BooleanField(
        required=False,
        allow_null=True
    )
    respondent_name: serializers.CharField = serializers.CharField(
        max_length=200, 
        required=False, 
        allow_blank=True
    )
    respondent_id_number: serializers.CharField = serializers.CharField(
        max_length=50, 
        required=False, 
        allow_blank=True
    )
    respondent_email: serializers.EmailField = serializers.EmailField(
        required=False, 
        allow_blank=True
    )
    respondent_phone: serializers.CharField = serializers.CharField(
        max_length=20, 
        required=False, 
        allow_blank=True
    )
    respondent_signature: serializers.CharField = serializers.CharField(
        required=False, 
        allow_blank=True
    )