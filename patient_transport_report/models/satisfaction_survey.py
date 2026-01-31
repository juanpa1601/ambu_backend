from django.db import models
from core.models import AuditedModel

class SatisfactionSurvey(AuditedModel):

    satisfaction_survey_conducted = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if the satisfaction survey was conducted'
    )
    ambulance_request_ease = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Ease of requesting the ambulance service'
    )
    phone_support_quality = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Quality of phone support received'
    )
    service_punctuality = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Punctuality of the ambulance service'
    )
    clear_info_provided = models.CharField(
        max_length=100,
        null=True,    
        blank=True,
        help_text='Clarity of information provided about the service'
    )
    staff_appearance = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Professional appearance of the ambulance staff'
    )
    ambulance_cleanliness = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Cleanliness of the ambulance'
    )
    driving_quality = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Quality of driving during the transport'
    )
    return_trip_timeliness = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Timeliness of the return trip'
    )
    safety_and_reassurance = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Feeling of safety and reassurance provided by the staff'
    )
    staff_empathy = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Empathy shown by the ambulance staff'
    )
    overall_satisfaction = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Overall satisfaction with the ambulance service'
    )
    would_recommend = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Likelihood of recommending the service to others'
    )
    comments = models.TextField(
        blank=True,
        null=True,
        help_text='Additional comments or suggestions from the respondent'
    )
    respondent_can_sign = models.BooleanField(
        null=True,
        blank=True,
        help_text='Indicates if the respondent is able to sign the survey'
    )
    respondent_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='Name of the respondent'
    )
    respondent_id_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='ID number of the respondent'
    )
    respondent_email = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
        help_text='Email address of the respondent'
    )
    respondent_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,    
        help_text='Phone number of the respondent'
    )
    respondent_signature = models.TextField(
        blank=True,
        null=True,
        help_text='Digital signature of the respondent in base64 format'
    )

    class Meta:
        verbose_name = 'Satisfaction Survey'
        verbose_name_plural = 'Satisfaction Surveys'