from django.core.validators import MaxValueValidator
from django.db import models


class Pediatric(models.Model):
    pediatric_nasal_cannula = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Pediatric nasal cannula quantity",
    )
    pediatric_simple_mask = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Pediatric simple mask quantity",
    )
    pediatric_non_rebreather_mask = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Pediatric non-rebreather mask quantity",
    )
    pediatric_venturi_system = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Pediatric venturi system quantity",
    )
    pediatric_nebulizer_kit = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Pediatric nebulizer kit quantity",
    )
    pediatric_bvm_bag_valve_mask = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Pediatric BVM bag valve mask quantity",
    )
    suction_bulb_aspirator = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Suction bulb aspirator quantity",
    )
    pediatric_sphygmomanometer = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Pediatric sphygmomanometer quantity",
    )
    oropharyngeal_airway_0 = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Oropharyngeal airway #0 quantity",
    )
    oropharyngeal_airway_1 = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Oropharyngeal airway #1 quantity",
    )
    oropharyngeal_airway_2 = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Oropharyngeal airway #2 quantity",
    )
    laryngeal_mask_1_5 = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Laryngeal mask 1.5 quantity",
    )
    laryngeal_mask_2 = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Laryngeal mask #2 quantity",
    )
    laryngeal_mask_3 = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Laryngeal mask #3 quantity",
    )
    umbilical_cord_clamp = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text="Umbilical cord clamp quantity",
    )

    def __str__(self):
        return f"Pediatric #{self.pk}"
