from django.db import models
from django.core.validators import MaxValueValidator


class Circulatory(models.Model):
    saline_solution_09_500cc = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Saline solution 0.9% 500cc quantity"
    )
    dextrose_5_percent = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Dextrose 5% quantity"
    )
    dextrose_10_percent = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Dextrose 10% quantity"
    )
    hartmann_lactate_solution = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Hartmann lactate solution quantity"
    )
    macro_drip_set = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Macro drip set quantity"
    )
    micro_drip_set = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Micro drip set quantity"
    )
    sterile_water = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Sterile water quantity"
    )
    syringe_1cc = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Syringe 1cc quantity"
    )
    syringe_3cc = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Syringe 3cc quantity"
    )
    syringe_5cc = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(20)],
        help_text="Syringe 5cc quantity"
    )
    syringe_10cc = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Syringe 10cc quantity"
    )
    syringe_20cc = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Syringe 20cc quantity"
    )
    syringe_50cc = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Syringe 50cc quantity"
    )
    iv_catheter_14g = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="IV catheter 14G quantity"
    )
    iv_catheter_16g = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="IV catheter 16G quantity"
    )
    iv_catheter_18g = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="IV catheter 18G quantity"
    )
    iv_catheter_20g = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="IV catheter 20G quantity"
    )
    iv_catheter_22g = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="IV catheter 22G quantity"
    )
    iv_catheter_24g = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="IV catheter 24G quantity"
    )
    scalp_vein_set_21g = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Scalp vein set 21G quantity"
    )
    scalp_vein_set_22g = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Scalp vein set 22G quantity"
    )
    scalp_vein_set_23g = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Scalp vein set 23G quantity"
    )
    sharps_container = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Sharps container quantity"
    )

    def __str__(self):
        return f"Circulatory #{self.pk}"
