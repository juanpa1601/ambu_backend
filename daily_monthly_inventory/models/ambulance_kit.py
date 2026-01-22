from django.core.validators import MaxValueValidator
from django.db import models


class AmbulanceKit(models.Model):
    trauma_shears = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Trauma shears quantity",
    )
    sterile_gauze_kit = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Sterile gauze kit quantity",
    )
    iv_tourniquet = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="IV tourniquet quantity",
    )
    hemorrhage_control_tourniquet = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Hemorrhage control tourniquet quantity",
    )
    medical_penlight = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Medical penlight quantity",
    )
    micropore_tape = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Micropore tape quantity",
    )
    adhesive_tape = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Adhesive tape quantity",
    )
    surgical_masks = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Surgical masks quantity",
    )
    n95_masks = models.IntegerField(
        default=0, validators=[MaxValueValidator(20)], help_text="N95 masks quantity"
    )
    alcohol_pads = models.IntegerField(
        default=0, validators=[MaxValueValidator(20)], help_text="Alcohol pads quantity"
    )
    eye_patches = models.IntegerField(
        default=0, validators=[MaxValueValidator(20)], help_text="Eye patches quantity"
    )
    tongue_depressors = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Tongue depressors quantity",
    )
    cotton_tipped_applicators = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Cotton-tipped applicators quantity",
    )
    clinical_thermometer = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Clinical thermometer quantity",
    )
    sanitary_pads = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Sanitary pads quantity",
    )

    def __str__(self):
        return f"AmbulanceKit #{self.pk}"
