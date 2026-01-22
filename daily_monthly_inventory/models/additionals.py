from django.core.validators import MaxValueValidator
from django.db import models


class Additionals(models.Model):
    tablet = models.IntegerField(
        default=0, validators=[MaxValueValidator(10)], help_text="Tablet quantity"
    )
    charger = models.IntegerField(
        default=0, validators=[MaxValueValidator(10)], help_text="Charger quantity"
    )
    data_clipboard_board = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Data clipboard board quantity",
    )
    medical_record_forms = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Medical record forms quantity",
    )
    cleaning_log_form = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Cleaning log form quantity",
    )
    temperature_log_form = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Temperature log form quantity",
    )
    artificial_tears = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Artificial tears quantity",
    )
    observations_comments = models.TextField(
        blank=True, default="", help_text="Observations and comments"
    )

    def __str__(self):
        return f"Additionals #{self.pk}"
