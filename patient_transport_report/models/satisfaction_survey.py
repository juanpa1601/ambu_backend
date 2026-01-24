from django.db import models

class SatisfactionSurvey(models.Model):

    ambulance_request_ease = models.CharField(max_length=100)
    phone_support_quality = models.CharField(max_length=100)
    service_punctuality = models.CharField(max_length=100)
    clear_info_provided = models.CharField(max_length=100)
    staff_appearance = models.CharField(max_length=100)
    ambulance_cleanliness = models.CharField(max_length=100)
    driving_quality = models.CharField(max_length=100)
    return_trip_timeliness = models.CharField(max_length=100)
    safety_and_reassurance = models.CharField(max_length=100)
    staff_empathy = models.CharField(max_length=100)
    overall_satisfaction = models.CharField(max_length=100)
    would_recommend = models.CharField(max_length=100)
    comments = models.TextField(
        blank=True,
        null=True
    )
    respondent_can_sign = models.BooleanField(default=True)
    respondent_name = models.CharField(max_length=200)
    respondent_id_number = models.CharField(max_length=100)
    respondent_email = models.EmailField(
        max_length=254,
        blank=True,
        null=True
    )
    respondent_phone = models.CharField(max_length=20)
    respondent_signature = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Satisfaction Survey'
        verbose_name_plural = 'Satisfaction Surveys'