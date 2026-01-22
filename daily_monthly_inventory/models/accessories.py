from django.db import models
from django.core.validators import MaxValueValidator


class Accessories(models.Model):
    eucida_advanced_disinfectant = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Eucida advanced disinfectant quantity",
    )
    wypall_towels = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Wypall towels quantity",
    )
    patient_blanket = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Patient blanket quantity",
    )
    stretcher_sheet = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Stretcher sheet quantity",
    )
    gloves_boxes = models.IntegerField(
        default=0, validators=[MaxValueValidator(10)], help_text="Gloves boxes quantity"
    )
    chemical_attack_kit_forms = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Chemical attack kit forms quantity",
    )
    chemical_attack_kit_ph_tape = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Chemical attack kit pH tape quantity",
    )
    adult_pediatric_stethoscope = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Adult/pediatric stethoscope quantity",
    )
    adult_sphygmomanometer = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Adult sphygmomanometer quantity",
    )
    white_waste_bags = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="White waste bags quantity",
    )
    red_biohazard_bags = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Red biohazard bags quantity",
    )
    clean_gauze_pack = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Clean gauze pack quantity",
    )
    red_biohazard_container = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Red biohazard container quantity",
    )
    white_waste_container = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="White waste container quantity",
    )
    wheelchair = models.IntegerField(
        default=0, validators=[MaxValueValidator(10)], help_text="Wheelchair quantity"
    )
    short_spinal_board = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Short spinal board quantity",
    )
    male_urinal = models.IntegerField(
        default=0, validators=[MaxValueValidator(10)], help_text="Male urinal quantity"
    )
    female_urinal = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Female urinal quantity",
    )
    thermo_hygrometer = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Thermo hygrometer quantity",
    )

    def __str__(self):
        return f"Accessories #{self.pk}"
